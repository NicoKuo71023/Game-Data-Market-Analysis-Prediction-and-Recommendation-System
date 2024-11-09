import requests
import json
from requests.auth import HTTPBasicAuth

class ElasticsearchQuery:
    """
    This class, `ElasticsearchQuery`, manages querying an Elasticsearch index, supporting optional API key authentication.

    1. Initialization:
    - Sets up the Elasticsearch host, index name, and optional API key.

    2. `get_auth` Method:
    - Returns HTTP basic authentication if an API key is provided, otherwise returns None.

    3. `get_count` Method:
    - Queries the index to retrieve the total document count using the `_count` endpoint.
    - Returns the document count or None if there is an error.

    4. `search_with_size` Method:
    - Retrieves the document count and uses it to set the `size` parameter for a `_search` request.
    - Executes a POST request with a query and returns all documents in the index up to the count limit.
    - Returns the query results or None if there is an error.

    Example usage:
    - Defines Elasticsearch host, index, and optional API key.
    - Initializes `ElasticsearchQuery`, defines a `match_all` query, and retrieves all documents in the index.
    """

    def __init__(self, es_host, index_name, api_key=None):
        self.es_host = es_host
        self.index_name = index_name
        self.api_key = api_key  # API key 是可選的

    def get_auth(self):
        """根據是否有 API key 返回適當的身份驗證方法"""
        if self.api_key:
            return HTTPBasicAuth(self.api_key[0], self.api_key[1])
        return None  # 如果沒有 API key，返回 None

    def get_count(self):
        # 構建 _count 請求的 URL
        endpoint = f'/{self.index_name}/_count'
        url = f'{self.es_host}{endpoint}'
        
        # 發送 GET 請求，根據是否有 API key 決定是否帶上身份驗證
        response = requests.get(url, auth=self.get_auth())
        
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
        
        # 發送 POST 請求進行查詢，根據是否有 API key 決定是否帶上身份驗證
        response = requests.post(url, headers={"Content-Type": "application/json"},
                                 data=json.dumps(query), auth=self.get_auth())
        
        # 檢查回應狀態碼並返回查詢結果
        if response.status_code == 200:
            dataset = json.loads(response.text)["hits"]["hits"]
            return [item["_source"] for item in dataset]
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None


if __name__ == "__main__":
    # 定義 Elasticsearch 雲端伺服器和索引
    es_host = 'https://e32aaa94f81549368f75827f1e5da659.us-central1.gcp.cloud.es.io/'
    index_name = 'game_data_aaa'
    
    # 你可以選擇是否提供 API key
    api_key = ("g1i_hJIBR8AYR_FZHqsZ", "NgU5E6CkSJmd1t8uuljJJA")  # 或者設置為 None
    
    # 初始化 ElasticsearchQuery 類
    es_query = ElasticsearchQuery(es_host, index_name, api_key)
    
    # 定義查詢的 query
    query = {
        "query": {
            "match_all": {}
        }
    }
    
    # 獲取資料庫大小並進行查詢
    search_result = es_query.search_with_size(query)
    
    # 顯示查詢結果
    if search_result:
        print(search_result[0])  # 顯示第一個結果
