import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import MinMaxScaler, PowerTransformer


class XGBoostModel:
    def __init__(self, model_path):
        """初始化，讀取 XGBoost 模型並獲取所需特徵"""
        self.model = xgb.Booster()
        self.model.load_model(model_path)

        # 獲取模型需要的特徵
        self.required_features = self.model.feature_names

        # 初始化 scaler 和 power transformer
        self.scaler = MinMaxScaler()
        self.pt = PowerTransformer(method='yeo-johnson')
    
    def log1p_and_scale(self, df):
        """對數轉換和 Min-Max 正規化"""
        df = df.copy()
        df['medianRevenue'] = np.log1p(df['medianRevenue'])
        df['averageRevenue'] = np.log1p(df['averageRevenue'])

        columns_to_scale = []
        for col in ["price", "publishedGames", "medianRevenue", "averageRevenue"]:
            if col in df:
                columns_to_scale.append(col)

        df[columns_to_scale] = self.scaler.transform(df[columns_to_scale])
        return df

    def powerTransformer(self, df):
        """Power transformation"""
        df = df.copy()
        numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

        df[numeric_columns] = self.pt.transform(df[numeric_columns])
        return df

    # 用來生成價格區間的函數
    def generate_price_values(start, end, step=1, decimals=[0.00, 0.25, 0.50, 0.75, 0.99]):
        price_values = []
        for i in range(start, end + 1, step):
            for decimal in decimals:
                price_values.append(round(i + decimal, 2))  
        return sorted(set(price_values)) 

    
    def prepare_and_predict_with_price_range(self, input_data):
        """
        接收一筆資料，自動清理並擴展 price 到 0~100，返回擴展後所有資料的預測結果
        """
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])
        elif isinstance(input_data, list):
            input_data = pd.DataFrame(input_data)
        
        # 準備特徵，缺失特徵補 0
        prepared_data = pd.DataFrame(columns=self.required_features)
        for index, row in input_data.iterrows():
            prepared_row = row[self.required_features].copy()
            for feature in self.required_features:
                if feature not in row:
                    prepared_row[feature] = 0  # 補 0
            prepared_data.loc[index] = prepared_row

        # 生成 price 從 0 到 100 的範圍
        price_values = self.generate_price_values(0, 100)  # 101 個數據點（步長為 1）
        predictions = []

        for price in price_values:
            # 替換每個 price 值到資料中
            transformed_data = prepared_data.copy()
            transformed_data['price'] = price

            # 對數據進行與訓練一致的轉換
            transformed_data = self.log1p_and_scale(transformed_data)
            transformed_data = self.powerTransformer(transformed_data)

            # 預測每個擴展後資料的結果
            dmatrix = xgb.DMatrix(transformed_data)
            pred = self.model.predict(dmatrix)
            predictions.append((price, pred[0]))  # 每個 price 對應的預測結果

        return predictions  # 返回 price 與預測值的對應數據組合