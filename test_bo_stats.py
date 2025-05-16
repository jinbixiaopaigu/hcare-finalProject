import json
from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterOperatorType, FilterCondition, FilterLogicType

def main():
    """获取华为Research表的数据统计和字段结构"""
    try:
        # 初始化客户端
        access_key = "8942feae410e40b395594be6c5db5386"
        secret_key = "3795a19165ac7f96cb0fd3e9760455dc3c6b56dacfd9f4a49f4a6b1abe5861e0"
        bridge_config = BridgeConfig("product", access_key, secret_key)
        http_config = HttpClientConfig(connect_timeout=200, read_timeout=200, retry_on_fail=True)
        bridge_client = BridgeClient(bridge_config, http_config)
        
        # 获取项目信息
        print("\n获取项目信息...")
        projects = bridge_client.get_bridgedata_provider().list_projects()
        
        if not projects:
            print("未找到项目")
            return
        
        project = projects[0]
        project_id = project.get('projectId')
        project_name = project.get('projectName')
        print(f"\n使用项目: {project_name} (ID: {project_id})")
        
        # 血氧饱和度表统计
        print("\n--- 血氧饱和度数据表统计 ---")
        bo_table_id = 't_mnhqsfbc_bloodoxygensaturation_system'
        print(f"查询表 {bo_table_id} 数据统计信息...")
        query_table_stats(bridge_client, bo_table_id, project_id)
        
        # 连续血氧表统计
        print("\n--- 连续血氧数据表统计 ---")
        cbo_table_id = 't_mnhqsfbc_continuousbloodoxygensaturation_system'  # 正确的表ID
        print(f"查询表 {cbo_table_id} 数据统计信息...")
        query_table_stats(bridge_client, cbo_table_id, project_id)
        
    except Exception as e:
        print(f"运行测试脚本失败: {str(e)}")

def query_table_stats(client, table_id, project_id):
    """查询表统计信息
    
    Args:
        client: 客户端实例
        table_id: 表ID
        project_id: 项目ID
        
    Returns:
        bool: 是否成功获取到数据
    """
    try:
        # 创建查询条件 - 确保使用非空条件
        condition = [FilterCondition("uniqueid", FilterOperatorType.EXISTS, True)]
        
        # 构造查询请求
        req = SearchTableDataRequest(
            table_id,
            filters=condition,
            desired_size=1000,
            project_id=project_id
        )
        
        results = []
        field_types = {}
        nested_fields = {}
        
        # 回调函数
        def query_callback(rows, total_cnt):
            print(f"查询到 {total_cnt} 条记录, 返回 {len(rows)} 条")
            if rows:
                results.extend(rows)
                
                # 分析第一条记录的字段类型
                first_record = rows[0]
                for key, value in first_record.items():
                    field_types[key] = type(value).__name__
                    if isinstance(value, dict):
                        nested_fields[key] = value
        
        # 执行查询
        client.get_bridgedata_provider().query_table_data(req, callback=query_callback)
        
        # 打印数据统计
        if results:
            print(f"\n总记录数: {len(results)} 条")
            
            # 打印字段类型
            print("\n表字段类型:")
            for field, type_name in field_types.items():
                print(f"  - {field}: {type_name}")
            
            # 打印嵌套字段结构
            for field, value in nested_fields.items():
                print(f"\n嵌套字段 '{field}' 的结构:")
                print_nested_structure(value, "  ")
            
            return True
        else:
            print("未获取到数据，可能是表为空或表名不正确")
            return False
            
    except Exception as e:
        print(f"查询失败: {str(e)}")
        return False

def print_nested_structure(obj, indent=""):
    """打印嵌套对象结构
    
    Args:
        obj: 嵌套对象
        indent: 缩进字符串
    """
    if not isinstance(obj, dict):
        print(f"{indent}- 值: {obj} (类型: {type(obj).__name__})")
        return
        
    for key, value in obj.items():
        if isinstance(value, dict):
            print(f"{indent}- {key} (嵌套对象):")
            print_nested_structure(value, indent + "  ")
        else:
            print(f"{indent}- {key}: {type(value).__name__}")

if __name__ == "__main__":
    main() 