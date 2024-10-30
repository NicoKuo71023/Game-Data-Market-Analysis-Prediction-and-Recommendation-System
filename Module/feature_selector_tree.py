from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import export_text

def feature_selector(full_table, tree_depth):
    X_full = full_table.drop(columns="sales").values
    Y_full = full_table['sales'].values
    X_train, X_test, y_train, y_test = train_test_split(X_full, Y_full, test_size=0.2, random_state=42)
    
    # 初始化決策樹回歸模型
    tree_regressor = DecisionTreeRegressor(max_depth=tree_depth)

    # 訓練模型
    tree_regressor.fit(X_train, y_train)
    y_pred = tree_regressor.predict(X_test)
    y_pred_train = tree_regressor.predict(X_train)
    # 評估模型
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    mse_train = mean_squared_error(y_train, y_pred_train)
    r2_train = r2_score(y_train, y_pred_train)
    # print(f'train Mean Squared Error (MSE): {mse_train}')
    # print(f'train R-squared (R²): {r2_train}')
    # print(f'test Mean Squared Error (MSE): {mse}')
    # print(f'test R-squared (R²): {r2}')
    feature_names = full_table.drop(columns="sales").columns.tolist()

    tree_text = export_text(tree_regressor, feature_names=feature_names)

    # 創建一個字典來存儲每一層的特徵名稱
    tree_layers = {}

    # 將每一行進行分割並根據縮排來判斷所屬層級
    for line in tree_text.split('\n'):
        # 計算每行的縮排，決定該行屬於第幾層 (| 表示層級)
        level = line.count('|')
        
        # 提取該行的特徵名稱，排除空行及沒有特徵名稱的行
        if '<=' in line or '>' in line:
            # 去除空格並找到 '--- ' 到 '<=' 或 '>' 之間的特徵名稱
            feature = line.split('--- ')[1].split(' <=')[0].split(' >')[0]
            
            # 將特徵名稱存儲在對應的層級中
            if level not in tree_layers:
                tree_layers[level] = []
            if feature not in tree_layers[level]:  # 防止重複加入
                tree_layers[level].append(feature)
    count=0
    # 顯示每一層的特徵名稱
    for level, features in tree_layers.items():
        # print(f"Level {level}: {features}")
        count += len(features)
    # print(count)
    features_set = set()

    # 只遍歷 key 1-6
    for level in range(1, tree_depth+1):
        if level in tree_layers:
            features_set.update(tree_layers[level])  # 使用 set 自動去重

    # 將 set 轉換為 tuple
    features_tuple = tuple(features_set)

    # 計算 tuple 裡的總數量
    total_features = len(features_set)

    # 顯示 tuple 和總數量
    # print(f"Features set: {features_set}")
    # print(f"Total number of features: {total_features}")
    # 提取 full_table 的第 5 列開始的所有列
    subset = full_table

    # 找到 subset 中與 feature_set 交集的列
    filtered_columns = subset.columns.intersection(features_set)

    # 只保留 feature_set 中存在的列
    filtered_subset = subset[filtered_columns]
    
    # 提取 full_table 的第一列
    first_column = full_table.iloc[:, :1]

    # 將第一列與 filtered_subset 合併
    new_table = pd.concat([first_column, filtered_subset], axis=1)
    return new_table