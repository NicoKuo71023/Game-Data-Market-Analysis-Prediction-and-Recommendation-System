import requests
import json

# 定義 Elasticsearch 的 URL 和索引
def ES_query(index_name, query):
    url = f"http://192.168.31.130:32327/{index_name}/_search"
    # 發送請求到 Elasticsearch
    response = requests.get(url, headers={"Content-Type": "application/json"}, data=json.dumps(query))
    # 檢查回應狀態碼並顯示結果
    if response.status_code == 200:
        result = response.json() 
    else:
        print(f"Error: {response.status_code}")
    return result

if __name__ == '__main__':
    query = {
        "size" : 752,
        "query": {
            "match_all": {}
        }
        }
    result = ES_query("game_data_aaa",query)
    print(result)