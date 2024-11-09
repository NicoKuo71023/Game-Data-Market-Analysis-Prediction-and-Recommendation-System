from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from g3_sql_class import SqlQuery
import pandas as pd
from recommond_game import recommond_game  ##  新增推薦系統
import json
import csv
import os
import re
from DL_model_class import PricingModel

app = Flask(
    __name__, static_folder="static", static_url_path="/static"
)  # 確保靜態文件夾路徑正確
CORS(app)
db = SqlQuery()  # 初始化 SqlQuery 類別


# # 連接到 Elasticsearch
es = Elasticsearch(["http://192.168.31.130:32327"])
indices = ["game_data_aaa", "game_data_aa", "game_data_indie"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/Dashboard")
def dashboard():
    # 返回你的 Dashboard 模板，確保這個模板存在
    return render_template("Dashboard.html")


@app.route("/game-info")
def game_info():
    steam_id = request.args.get("steamId")
    query = {"query": {"match": {"steamId": steam_id}}}
    response = es.search(index=",".join(indices), body=query)
    result = [hit["_source"] for hit in response["hits"]["hits"]]

    ### 嘗試增加推薦系統
    df_result = pd.DataFrame(
        db.sql_search("SELECT steamId, name, string FROM recommond")
    )
    recommond_games = recommond_game(df_result, int(steam_id))
    recommond_games_list = recommond_games.to_dict(orient="records")

    ### 嘗試增加推薦系統

    if result:
        return render_template(
            "GameInformation.html",
            game_info=result,
            steam_id=steam_id,
            recommond_games=recommond_games_list,
        )
    else:
        return render_template("GameInformation.html")


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 構建CSV檔案的絕對路徑
FEATURES_CSV = os.path.join(BASE_DIR, "features.csv")
GENRES_CSV = os.path.join(BASE_DIR, "genres.csv")
TAGS_CSV = os.path.join(BASE_DIR, "tags.csv")


# 讀取 CSV 文件的函數
def read_csv(file_path):
    with open(file_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        return [row[0] for row in reader]  # 假設每行只有一列資料


@app.route("/game-model")
def game_model():
    # 使用絕對路徑讀取 CSV 資料
    features = read_csv(FEATURES_CSV)
    genres = read_csv(GENRES_CSV)
    tags = read_csv(TAGS_CSV)

    # 傳遞資料到 GameModel 模板
    return render_template(
        "GameModel.html", features=features, genres=genres, tags=tags
    )


@app.route("/search", methods=["GET"])
def search():
    steam_id = request.args.get("steamId")
    # 查找匹配的遊戲數據
    query = {"query": {"match": {"steamId": steam_id}}}
    response = es.search(index=",".join(indices), body=query)
    result = [hit["_source"] for hit in response["hits"]["hits"]]
    return jsonify(result)


@app.route("/search-game", methods=["GET"])
def search_game():
    query = request.args.get("q", "")
    sql = f"SELECT steamId, name FROM main WHERE name LIKE '%{query}%'"
    results = db.sql_search(sql)
    return jsonify(results)


# 移除箭頭符號的處理函數
def sanitize_input(value):
    # 如果是字符串，處理箭頭符號和其他特殊符號
    if isinstance(value, str):
        value = value.replace("⭹", "")  # 移除特定箭頭符號
        # 使用正則表達式過濾掉特殊符號，保留字母、數字、空格、逗號、點和破折號
        value = re.sub(
            r"[^\w\s,.-]", "", value
        )  # 只保留字母、數字、空格、逗號、點和破折號
    return value


@app.route("/submit-game", methods=["POST"])
def submit_game():
    print("Received POST request at /submit-game")
    form_data = request.form

    # 將表單數據轉換為字典
    game_data = {
        "publishedGames": float(sanitize_input(form_data.get("publishedGames"))),
        "averageRevenue": float(sanitize_input(form_data.get("averageRevenue"))),
        "medianRevenue": float(sanitize_input(form_data.get("medianRevenue"))),
        "totalRevenue": float(sanitize_input(form_data.get("totalRevenue"))),
        "features": list(set(sanitize_input(form_data.get("features")).split(","))),
        "genres": list(set(sanitize_input(form_data.get("genres")).split(","))),
        "tags": list(set(sanitize_input(form_data.get("tags")).split(","))),
    }

    # 加載模型並進行預測
    model_path = "./DNN_model_for_pricing"
    pricing_model = PricingModel(model_path)

    pred_list = pricing_model.prepare_and_predict_with_price_range(game_data)

    # 直接返回預測結果，無需保存到文件
    return jsonify({"message": "資料已提交！", "data": pred_list})


# 接模型吐回的數據
@app.route("/predict", methods=["GET"])
def predict_pic():
    with open("game_data.json", "r") as json_file:
        result = json.load(json_file)  # 加入 json_file 作為參數
    return jsonify(result)


# 接模型吐回的數據


if __name__ == "__main__":
    app.run(debug=True)
