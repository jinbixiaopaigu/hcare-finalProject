import json
from huaweiresearchsdk.bridge import BridgeClient
from huaweiresearchsdk.config import BridgeConfig, HttpClientConfig
from huaweiresearchsdk.model.table import SearchTableDataRequest, FilterOperatorType, FilterCondition

def main():
    # u521du59cbu5316u5ba2u6237u7aef
    access_key = "8942feae410e40b395594be6c5db5386"
    secret_key = "3795a19165ac7f96cb0fd3e9760455dc3c6b56dacfd9f4a49f4a6b1abe5861e0"
    bridge_config = BridgeConfig("product", access_key, secret_key)
    http_config = HttpClientConfig(connect_timeout=200, read_timeout=200, retry_on_fail=True)
    bridge_client = BridgeClient(bridge_config, http_config)
    
    # u83b7u53d6u9879u76eeu4fe1u606f
    print("\nu83b7u53d6u9879u76eeu4fe1u606f...")
    projects = bridge_client.get_bridgedata_provider().list_projects()
    
    if not projects:
        print("\u672au627eu5230u9879u76ee")
        return
    
    project = projects[0]
    project_id = project.get('projectId')
    print(f"\nu4f7fu7528u9879u76ee: {project.get('projectName')} (ID: {project_id})")
    
    # u67e5u8be2u623fu98a4u6d4bu91cfu7ed3u679cu8868
    table_id = 't_mnhqsfbc_atrialfibrillationmeasureresult_system'
    print(f"\nu67e5u8be2u8868 {table_id} u6570u636e...")
    
    # u521bu5efau67e5u8be2u6761u4ef6
    condition = [FilterCondition("id", FilterOperatorType.EXISTS, True)]
    
    # u6784u9020u67e5u8be2u8bf7u6c42
    req = SearchTableDataRequest(
        table_id,
        filters=condition,
        desired_size=100,
        project_id=project_id
    )
    
    results = []
    
    # u56deu8c03u51fdu6570
    def query_callback(rows, total_cnt):
        print(f"\nu67e5u8be2u5230 {total_cnt} u6761u8bb0u5f55, u8fd4u56de {len(rows)} u6761")
        if rows:
            results.extend(rows)
            print("\nu7b2cu4e00u6761u8bb0u5f55:")
            print(json.dumps(rows[0], indent=2, ensure_ascii=False))
            # u5217u51fau6240u6709u5b57u6bb5
            print("\nu5b57u6bb5u5217u8868:")
            for key in rows[0].keys():
                print(f"- {key}")
    
    # u6267u884cu67e5u8be2
    bridge_client.get_bridgedata_provider().query_table_data(req, callback=query_callback)
    
    if not results:
        print("\u672au627eu5230u6570u636e")
    
    # u5c1du8bd5u4e0du540cu7684u67e5u8be2u65b9u5f0f
    print("\nu5c1du8bd5u4f7fu7528u5176u5b83u5b57u6bb5u67e5u8be2...")
    alt_conditions = [
        FilterCondition("uniqueid", FilterOperatorType.EXISTS, True),
    ]
    
    alt_req = SearchTableDataRequest(
        table_id,
        filters=alt_conditions,
        desired_size=100,
        project_id=project_id
    )
    
    bridge_client.get_bridgedata_provider().query_table_data(alt_req, callback=query_callback)

if __name__ == "__main__":
    main() 