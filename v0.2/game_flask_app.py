from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from g3_sql_class import SqlQuery

app = Flask(
    __name__, static_folder="static", static_url_path="/static"
)  # 確保靜態文件夾路徑正確
CORS(app)
db = SqlQuery()  # 初始化 SqlQuery 類別


# 連接到 Elasticsearch
es = Elasticsearch(["http://192.168.31.130:32327"])
indices = ["game_data_aaa", "game_data_aa", "game_data_indie"]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game-info")
def game_info():
    steam_id = request.args.get("steamId")
    query = {"query": {"match": {"steamId": steam_id}}}
    response = es.search(index=",".join(indices), body=query)
    result = [hit["_source"] for hit in response["hits"]["hits"]]
    if result:
        return render_template(
            "GameInformation.html", game_info=result, steam_id=steam_id
        )
    else:
        return render_template("GameInformation.html")


@app.route("/game-model")
def game_model():
    return render_template("GameModel.html")


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


if __name__ == "__main__":
    app.run(debug=True)
