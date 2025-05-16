import requests
import json

def test_cbo_list_api():
    """测试连续血氧数据列表API"""
    url = "http://localhost:5000/medical/cbo/list"
    params = {
        "page": 1,
        "pageSize": 10
    }
    
    try:
        print(f"发送请求: {url}")
        response = requests.get(url, params=params)
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("响应数据:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # 验证响应结构
            if "rows" in data:
                print(f"数据列表条数: {len(data['rows'])}")
            if "total" in data:
                print(f"数据总数: {data['total']}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求异常: {str(e)}")

if __name__ == "__main__":
    test_cbo_list_api() 