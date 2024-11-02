import pandas as pd
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 主程式
def recommond_game(df_result, user_input):
    
    def genres_and_tags_to_string(row):
        tags = row["genres"]
        tags = " ".join([j for j in tags])

        features = row["tags"]
        features = " ".join([j for j in features])
        return tags + " " + features

    # 將genres和tags轉換為字串格式
    df_result["string"] = df_result.apply(genres_and_tags_to_string, axis=1)

    # 使用 tfidf
    tfidf = TfidfVectorizer(max_features=2000)
    tfidf_matrix = tfidf.fit_transform(df_result["string"])

    # 將steamId對應index
    game2idx = pd.Series(df_result.index, index=df_result["steamId"])

    # 檢查steamId是否存在
    if user_input not in game2idx:
        return "Steam ID 不存在於資料中。"

    # 存取該指定遊戲的向量值
    idx = game2idx[user_input]
    query_game = tfidf_matrix[idx]

    # 計算相似程度
    scores = cosine_similarity(query_game, tfidf_matrix).ravel()

    # 總結最像的前5名遊戲
    recommended_idx = scores.argsort()[-6:-1][::-1]

    # 返還最終查詢結果
    recommond_result = df_result[["steamId", "name"]].iloc[recommended_idx].reset_index(drop=True)

    return recommond_result


# 讀取資料 (測試用)
# df = pd.read_json(r"C:\Users\student\Desktop\BDSE35_final_project\src\Data_analysis\Local_market_analysis\df.json")

# AAA = pd.read_csv(r'C:\Users\student\Desktop\BDSE35_final_project\data\AAA\main_aaa.csv')
# AA = pd.read_csv(r'C:\Users\student\Desktop\BDSE35_final_project\data\AA\main_aa.csv')
# Indie = pd.read_csv(r'C:\Users\student\Desktop\BDSE35_final_project\data\Indie\main_indie.csv')

# AAA = AAA[['steamId', 'name']]
# AA = AA[['steamId', 'name']]
# Indie = Indie[['steamId', 'name']]

# steamId_name = pd.concat([AAA, AA, Indie], axis=0).reset_index(drop=True)

# 合併資料
# df_result = pd.merge(df, steamId_name, on='steamId', how='inner')

# 測試
# print(recommond_game(df_result, 359550))
