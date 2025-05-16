import json
from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterOperatorType, FilterCondition

def main():
    """获取华为Research表的数据统计和字段结构"""
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
    
    # 查询血氧饱和度表
    table_id = 't_mnhqsfbc_bloodoxygensaturation_system'
    print(f"\n查询表 {table_id} 数据统计信息...")
    
    # 创建查询条件 - 确保使用非空条件
    condition = [FilterCondition("uniqueid", FilterOperatorType.EXISTS, True)]
    
    # 构造查询请求
    req = SearchTableDataRequest(
        table_id,
        filters=condition,
        desired_size=10,  # 只获取少量数据用于分析
        project_id=project_id
    )
    
    results = []
    field_counts = {}  # 用于统计字段的填充率
    field_types = {}   # 用于存储字段类型
    
    # 回调函数
    def query_callback(rows, total_cnt):
        print(f"\n查询到 {total_cnt} 条记录, 返回 {len(rows)} 条")
        if rows:
            results.extend(rows)
            
            # 分析第一条记录，获取字段结构
            if len(results) == 1:
                sample_record = results[0]
                print("\n表字段结构:")
                
                # 分析扁平字段
                for key, value in sample_record.items():
                    field_type = type(value).__name__
                    field_types[key] = field_type
                    
                    # 初始化字段计数
                    field_counts[key] = 0
                
                # 分析嵌套字段 (例如 oxygenSaturation)
                for key, value in sample_record.items():
                    if isinstance(value, dict):
                        print(f"  - {key} (嵌套对象):")
                        _analyze_nested_field(key, value, "    ")
                    else:
                        print(f"  - {key}: {field_types[key]}")
            
            # 统计字段填充率
            for record in rows:
                for field in field_counts.keys():
                    if field in record and record[field] is not None:
                        field_counts[field] += 1
    
    # 分析嵌套字段的辅助函数
    def _analyze_nested_field(parent_key, obj, indent):
        if not isinstance(obj, dict):
            return
        
        for key, value in obj.items():
            full_key = f"{parent_key}.{key}"
            
            if isinstance(value, dict):
                print(f"{indent}- {key} (嵌套对象):")
                _analyze_nested_field(full_key, value, indent + "  ")
            else:
                field_type = type(value).__name__
                print(f"{indent}- {key}: {field_type}")
    
    # 执行查询
    print("\n正在执行查询，请稍候...")
    bridge_client.get_bridgedata_provider().query_table_data(req, callback=query_callback)
    
    if not results:
        print("\n警告：未能获取到数据，可能表为空或表名不正确")
        return
    
    # 计算和显示字段填充率
    print("\n字段填充率统计 (基于查询结果):")
    total_records = len(results)
    for field, count in field_counts.items():
        fill_rate = (count / total_records) * 100
        print(f"  - {field}: {count}/{total_records} ({fill_rate:.1f}%)")
    
    # 生成转换映射建议
    print("\n建议的字段映射 (不含具体数据值):")
    field_mapping = {}
    for key in results[0].keys():
        # 转换为snake_case风格，适应MySQL表
        snake_case = key
        # 将驼峰式转为下划线式
        if key[0].islower() and any(c.isupper() for c in key):
            snake_case = ''.join(['_'+c.lower() if c.isupper() else c for c in key])
        
        field_mapping[key] = snake_case
    
    print(json.dumps(field_mapping, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main() 