import requests
import json

class ElasticsearchQuery:
    def __init__(self, es_host, index_name):
        self.es_host = es_host
        self.index_name = index_name

    def get_count(self):
        # 構建 _count 請求的 URL
        endpoint = f'/{self.index_name}/_count'
        url = f'{self.es_host}{endpoint}'
        
        # 發送 GET 請求
        response = requests.get(url)
        
        # 檢查回應狀態碼並返回 count 值
        if response.status_code == 200:
            return json.loads(response.text).get("count")
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def search_with_size(self, query):
        # 根據 _count 查詢結果來設定 _search 的 size
        count = self.get_count()
        if count is None:
            print("Failed to get the count. Search aborted.")
            return
        
        # 構建 _search 請求的 URL
        endpoint = f'/{self.index_name}/_search'
        url = f'{self.es_host}{endpoint}'
        
        # 更新 query，設定 size 為 count
        query['size'] = count
        
        # 發送 POST 請求進行查詢
        response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(query))
        
        # 檢查回應狀態碼並返回查詢結果
        if response.status_code == 200:
            dataset = json.loads(response.text)["hits"]["hits"]
            return [item["_source"] for item in dataset]
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None


