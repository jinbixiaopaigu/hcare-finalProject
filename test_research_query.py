import json
from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterOperatorType, FilterCondition

def main():
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
    print(f"\n使用项目: {project.get('projectName')} (ID: {project_id})")
    
    # 查询血氧饱和度表
    table_id = 't_mnhqsfbc_bloodoxygensaturation_system'
    print(f"\n查询表 {table_id} 数据...")
    
    # 创建查询条件 - 确保使用非空条件
    condition = [FilterCondition("uniqueid", FilterOperatorType.EXISTS, True)]
    
    # 构造查询请求
    req = SearchTableDataRequest(
        table_id,
        filters=condition,
        desired_size=5,  # 只需要少量记录就能验证字段
        project_id=project_id
    )
    
    results = []
    
    # 回调函数
    def query_callback(rows, total_cnt):
        print(f"\n查询到 {total_cnt} 条记录, 返回 {len(rows)} 条")
        if rows:
            results.extend(rows)
            print("\n第一条记录:")
            print(json.dumps(rows[0], indent=2, ensure_ascii=False))
            # 列出所有字段
            print("\n字段列表及值类型:")
            for key, value in rows[0].items():
                value_type = type(value).__name__
                print(f"- {key}: {value_type}")
    
    # 执行查询
    bridge_client.get_bridgedata_provider().query_table_data(req, callback=query_callback)
    
    if not results:
        print("未找到数据，尝试其他条件...")
        # 尝试另一个字段
        alt_condition = [FilterCondition("healthid", FilterOperatorType.EXISTS, True)]
        alt_req = SearchTableDataRequest(
            table_id,
            filters=alt_condition,
            desired_size=5,
            project_id=project_id
        )
        bridge_client.get_bridgedata_provider().query_table_data(alt_req, callback=query_callback)

    # 如果还是没有数据，打印提示信息
    if not results:
        print("\n警告：未能获取到数据，可能表为空或表名不正确")
    else:
        # 打印字段映射建议
        print("\n建议的字段映射:")
        field_mapping = {}
        for key in results[0].keys():
            # 转换为snake_case风格，适应MySQL表
            snake_case = key
            # 将驼峰式转为下划线式
            if key[0].islower() and any(c.isupper() for c in key):
                snake_case = ''.join(['_'+c.lower() if c.isupper() else c for c in key])
            
            field_mapping[key] = snake_case
        
        print(json.dumps(field_mapping, indent=4, ensure_ascii=False))
        print("\n以上映射仅为建议，请根据实际情况调整")

if __name__ == "__main__":
    main() 