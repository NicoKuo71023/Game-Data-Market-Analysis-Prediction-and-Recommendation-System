from elasticsearch import Elasticsearch


class EsSearch:

    def __init__(self, host="http://192.168.31.130:32327"):
        self.es = Elasticsearch(host)

    def search_from_id(self, id):
        """
        從ES上抓下與指定 steamId 匹配的原始資料
        """
        scroll_size = 1000
        scroll_time = "2m"
        list_index = ["game_data_aaa", "game_data_aa", "game_data_indie"]

        all_hits = []
        for index_name in list_index:
            res = self.es.search(
                index=index_name,
                scroll=scroll_time,
                size=scroll_size,
                body={
                    "query": {"term": {"steamId": id}},
                },
            )

            scroll_id = res["_scroll_id"]
            all_hits.extend(res["hits"]["hits"])

            while len(res["hits"]["hits"]) > 0:
                res = self.es.scroll(scroll_id=scroll_id, scroll=scroll_time)
                all_hits.extend(res["hits"]["hits"])

        return [doc["_source"] for doc in all_hits]
