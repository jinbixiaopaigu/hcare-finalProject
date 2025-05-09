import configparser
import json
from huaweiresearchsdk.bridge import BridgeClient 
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig 
from huaweiresearchsdk.model import AuthRequest
try:
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config.ini')
    
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
    
except configparser.Error as e:
    print(f"配置文件读取错误: {e}")
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
except Exception as e:
    print(f"操作错误: {str(e)}")