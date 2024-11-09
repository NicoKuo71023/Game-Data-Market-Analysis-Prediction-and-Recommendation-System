import csv

import numpy as np
import pandas as pd
import torch
import torch.nn as nn


class PricingModel:
    def __init__(
        self,
        model_path,
        input_size=487,
        hidden_layers=1,
        hidden_units=320,
        dropout_rate=0.8450569460998046,
    ):
        # 創建模型結構
        self.model = self.create_model(
            hidden_layers, hidden_units, dropout_rate, input_size
        )

        # 載入模型權重
        self.model.load_state_dict(torch.load(model_path))
        self.model.to("cpu")  # 如果後端不支持GPU，可以使用CPU

        # 設置為推理模式
        self.model.eval()

    def create_model(self, hidden_layers, hidden_units, dropout_rate, input_size):
        layers = [
            nn.Linear(input_size, 1024),  # 輸入層
            nn.ReLU(),
            nn.BatchNorm1d(1024),
            nn.Dropout(p=dropout_rate),  # 使用可調整的 dropout rate
        ]

        # 動態添加隱藏層
        in_features = 1024
        for _ in range(hidden_layers):
            layers.append(nn.Linear(in_features, hidden_units))
            layers.append(nn.ReLU())
            layers.append(nn.BatchNorm1d(hidden_units))
            layers.append(nn.Dropout(p=dropout_rate))
            in_features = hidden_units

        # 輸出層
        layers.append(nn.Linear(in_features, 1))

        return nn.Sequential(*layers)

    def one_hot_encode(self, input_data):
        columns = ["features", "genres", "tags"]

        for column in columns:
            input_data[column] = input_data[column].apply(
                lambda x: x if isinstance(x, list) else [x]
            )

        # 檢查 columns 是否為空或只有一個空字串，並刪除
        columns = [
            col
            for col in columns
            if input_data[col].explode().any()
            and not (input_data[col].explode() == "").all()
        ]

        # 確保只保留需要的欄位
        final_df = input_data[
            ["publishedGames", "averageRevenue", "medianRevenue", "totalRevenue"]
        ].copy()

        for column in columns:
            # 檢查該列的列表是否為空
            if input_data[column].apply(lambda x: len(x) == 0).any():
                # 如果有空的列表，則跳過這個欄位的處理
                continue

            # 使用 explode 將列展開
            exploded = input_data.explode(column)

            # 使用 get_dummies 進行 one-hot 編碼
            one_hot = pd.get_dummies(
                exploded[column].str.strip(), prefix="", dummy_na=False
            )

            # 檢查合併前的列名，確保不會重疊
            one_hot.columns = [
                f"{column}_{col}" if col else column for col in one_hot.columns
            ]

            # 合併 one-hot 編碼到 final_df，這裡要確保列名不會重疊
            final_df = final_df.join(one_hot.groupby(exploded.index).sum(), how="outer")

        # 移除原始的類別欄位
        final_df = final_df.loc[
            :, ~final_df.columns.isin(["features", "genres", "tags"])
        ]

        # 簡化列名，去除不必要的前綴
        final_df.columns = final_df.columns.str.replace(
            r"^[^_]*_", "", regex=True
        ).str.lstrip("_")

        # 返回最終的 DataFrame，僅包含需求的欄位
        return final_df

    def prepare_and_predict_with_price_range(self, input_data):
        """
        接收一筆資料，自動清理並擴展 price 到 0~100，返回擴展後所有資料的預測結果
        """

        # 將 input_data 轉換為 DataFrame 格式
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            input_data = pd.DataFrame(input_data)

        # 檢查需要的列是否存在
        required_columns = ["features", "genres", "tags"]
        for col in required_columns:
            if col not in input_data.columns:
                raise ValueError(f"Input data must contain the column: {col}")

        # One-hot 編碼
        input_data = self.one_hot_encode(input_data)

        with open("./req_col.csv", "r") as f:
            reader = csv.reader(f)
            req_col = next(reader)

        prepared_data = pd.DataFrame(0, index=[0], columns=req_col)
        prepared_data_lowered_columns = prepared_data.columns.str.lower()
        input_data_lowered_columns = input_data.columns.str.lower()

        matching_columns = [
            col
            for col in input_data_lowered_columns
            if col in prepared_data_lowered_columns
        ]

        for col in matching_columns:
            # 獲取原始列名以便填充值
            original_col_name = input_data.columns[input_data_lowered_columns == col][0]

            # 找到對應的全小寫列名在 prepared_data 中的索引
            matching_prepared_col = prepared_data.columns[
                prepared_data_lowered_columns == col
            ][0]

            # 將值填入 prepared_data 中對應的列
            prepared_data.loc[0, matching_prepared_col] = input_data.loc[
                0, original_col_name
            ]

        # publishedGames min: 1; publishedGames max: 489
        # medianRevenue min: 0.0;  medianRevenue max: 49019453.0
        # averageRevenue min: 145.53424657534248; averageRevenue max: 49019453.0
        prepared_data["publishedGames"] = (prepared_data["publishedGames"] - 1) / (
            489 - 1
        )
        prepared_data["medianRevenue"] = prepared_data["medianRevenue"] / 49019453.0
        prepared_data["averageRevenue"] = (
            prepared_data["averageRevenue"] - 145.53424657534248
        ) / (49019453.0 - 145.53424657534248)

        # return prepared_data

        # 創建 100 行的 DataFrame，複製原來的資料
        expanded_data = pd.DataFrame([prepared_data.iloc[0]] * 100)

        # 創建 price 欄位，並填充從 1 到 100 的數字
        expanded_data["price"] = list(range(1, 101))
        expanded_data["price"] = np.log1p(expanded_data["price"]) / 5.30325516

        # 確保所有欄位準備好後進行預測
        with torch.no_grad():  # 禁用梯度計算
            model_input = torch.tensor(expanded_data.values, dtype=torch.float32)
            prediction = self.model(model_input)

        predicted_sales = prediction

        price = expanded_data["price"].values
        x = np.expm1(price * 5.30325516)

        # 將預測結果移到 CPU 並轉換為 numpy 格式
        predicted_sales_log = predicted_sales.numpy()

        # 根據您使用的對數底數進行反對數運算
        # 如果是自然對數（底數為 e）
        predicted_sales = np.expm1(predicted_sales_log)

        # return predicted_sales_log

        key_obj = []
        for i in range(100):
            item = {"price": x[i], "predicted_sales": predicted_sales[i].item()}
            key_obj.append(item)

        key_obj = [
            {k: float(v) if isinstance(v, np.float32) else v for k, v in item.items()}
            for item in key_obj
        ]

        # 假設預測結果是價格，並返回
        return key_obj  # 將預測結果轉為數字並返回
