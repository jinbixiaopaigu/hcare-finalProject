import configparser
import json
from huaweiresearchsdk.bridge import BridgeClient 
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig 
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterOperatorType

class SimpleFilter:
    """用于模拟过滤器对象的简单类"""
    def __init__(self, field, operator, value):
        self.field = field
        self.operator = operator
        self.value = value

def process_query_result(rows, total_cnt):
    """具备防御性检查的回调函数"""
    # 类型安全检查
    if not isinstance(rows, list):
        print("错误：预期list类型，但得到：", type(rows))
        return

    print(f"共 {total_cnt} 条记录")
    
    # 处理空结果集
    if not rows:
        print("提示：查询返回空结果集")
        return

    # 安全处理记录（增加边界检查）
    try:
        max_display = min(len(rows), 5)
        for i in range(max_display):
            row = rows[i]
            if isinstance(row, dict):
                print(f"\n记录 {i+1}:", json.dumps(row, ensure_ascii=False))
            else:
                print(f"\n记录 {i+1} 格式异常")
    except Exception as e:
        print(f"处理记录时发生错误: {str(e)}")

try:
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    
    # 获取凭证信息
    access_key = config.get('credentials', 'access_key')
    secret_key = config.get('credentials', 'secret_key')

    # 初始化BridgeConfig类 
    bridgeconfig = BridgeConfig("product", access_key, secret_key) 

    # 连接超时时间，单位s，不设置则默认30s 
    connect_timeout = 200 

    # 等待接口返回超时时间，单位s，不设置则默认30s 
    read_timeout = 200 

    # 是否失败重试，默认不重试 
    retry_on_fail = True 

    # 初始化HttpClientConfig类 
    httpconfig = HttpClientConfig(connect_timeout, read_timeout, retry_on_fail) 

    bridgeclient = BridgeClient(bridgeconfig, httpconfig)
    
    # 添加验证输出
    print("华为Research SDK初始化成功！")
    print(f"使用的Access Key: {access_key[:4]}...{access_key[-4:]}")
    print(f"连接超时: {connect_timeout}s, 读取超时: {read_timeout}s")
    print(f"失败重试: {'是' if retry_on_fail else '否'}")
    print("httpconfig",httpconfig)
    print("bridgeclient",bridgeclient)
    
    # 获取项目信息
    print("\n获取用户加入的项目信息...")
    try:
        # 尝试获取原始响应
        print("尝试获取原始响应...")
        provider = bridgeclient.get_bridgedata_provider().list_projects()
        print(f"原始响应: {provider}")
        response = provider._http_client.get(provider._base_url + "/projects")  # 假设的API端点
        
        # 调试输出
        print(f"API响应状态码: {response.status_code}")
        print(f"原始响应内容: {response.text[:200]}...")  # 只打印前200字符
        
        # 手动解析JSON
        projects = json.loads(response.text)
        
        if not projects:
            print("警告：未找到任何项目")
        else:
            print("\n找到的项目列表：")
            for i, project in enumerate(projects, 1):
                print(f"\n项目 {i}:")
                print(f"ProjectId: {project.get('projectId', '无')}")
                print(f"ProjectCode: {project.get('projectCode', '无')}")
                print(f"项目名称: {project.get('projectName', '无')}")
                
    except AttributeError:
        # 如果直接调用list_projects()可用
        projects = bridgeclient.get_bridgedata_provider().list_projects()
        if not projects:
            print("警告：未找到任何项目")
        else:
            print("\n找到的项目列表：")
            for i, project in enumerate(projects, 1):
                print(f"\n项目 {i}:")
                print(f"ProjectId: {project.get('projectId', '无')}")
                print(f"ProjectCode: {project.get('projectCode', '无')}")
                print(f"项目名称: {project.get('projectName', '无')}")
    
    # 在项目列表获取后添加数据表查询
    if projects:
        first_project = projects[0]
        project_id = first_project.get('projectId')
        if project_id:
            print(f"\n正在查询项目 {project_id} 的 t_mnhqsfbc_atrialfibrillationmeasureresult_system 表数据...")
            
            # 使用SDK标准接口构造查询请求（加强空值处理）
            req = SearchTableDataRequest(
                index_name='t_mnhqsfbc_atrialfibrillationmeasureresult_system',
                project_id=project_id,
                desired_size=100,
                giveup_when_more_than=1000,
                filters=[
                    SimpleFilter(field="healthid", operator=FilterOperatorType.EXISTS, value=True)  # 添加安全过滤条件
                ]
            )
            
            # 通过SDK标准接口执行查询
            provider = bridgeclient.get_bridgedata_provider()
            
            # 添加完整的响应验证装饰器
            def safe_callback(rows, total):
                """完整的结果验证装饰器"""
                if not isinstance(total, (int, float)):
                    print("警告：total参数类型异常", type(total))
                    return
                
                if not isinstance(rows, list):
                    print("警告：rows参数类型异常", type(rows))
                    return
                
                if not rows:
                    print("API返回空结果集（无数据）")
                    return
                
                process_query_result(rows, total)

            provider.query_table_data(req, callback=safe_callback)
            
        else:
            print("项目ID为空，无法查询数据表")
    
except configparser.Error as e:
    print(f"配置文件读取错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
except Exception as e:
    print(f"操作错误: {str(e)}")