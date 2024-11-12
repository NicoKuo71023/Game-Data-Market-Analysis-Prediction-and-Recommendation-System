# GamaDigit - Game Data Explorer: Market Analysis, Prediction, and Recommendation System

## Project Overview

This project aims to conduct an in-depth analysis of the global game market, with a particular focus on the dynamics and player demands in the single-player game segment, while also developing a data-driven recommendation system. With the sustained growth of the global game market, single-player games continue to hold an important place, thanks to their innovation and immersive experience. By analyzing market data, studying player behavior, and exploring game genres, this project seeks to offer valuable insights to game developers and marketing teams.

## Project Objectives

- **Enhance Market Insight**: Provide developers with deep insights into player preferences and market demands.
- **Reduce Development Risks**: Minimize the risk of commercial failure by analyzing market demands and predicting the potential of new games through a recommendation system.
- **Increase Player Loyalty**: Boost player engagement and satisfaction by providing game recommendations tailored to player preferences.
- **Support Market Strategies**: Offer market trend analysis to assist companies in developing effective strategies, identifying “blue ocean” markets, and avoiding “red ocean” competition.

## System Architecture

- **Hardware Architecture**: Utilizes a Harvester Cluster/RKE2 (Kubernetes) setup, incorporating Elasticsearch clusters and MySQL databases.
- **Layered Service Architecture**: Comprises a data source layer, data processing and analysis layer, business application layer, and presentation layer.
- **Data Pipeline**: Includes data sources, data lake, and data warehouse with ETL and analysis processes, supporting computations for the recommendation system and market analysis.

## Recommendation System Mechanism

The recommendation system operates through the following process:

1. Generate textual vectors for game tags and genres using TF-IDF.
2. Calculate cosine similarity between games.
3. Rank and recommend the top 5 games that closely match user preferences.

## Market Analysis

### Global Market Trends

- Market revenue is projected to continue growing, with single-player games maintaining a significant market share and growth potential.
- Preferences lean towards specific game genres, such as action and adventure, particularly in major markets like the United States, China, and Russia.

### Game Genre Analysis

- Analyze the market performance of various game genres, tracking changes over the past 5-10 years in terms of game count, sales, and revenue.
- Provide region-specific market recommendations, helping developers understand the particular demands in different areas.

## Model Building

The model building for this project aims to predict a game’s first-month sales based on game features (such as tags and genres) and developer-related information. A variety of models will be compared, including linear regression, polynomial ridge regression, XGBoost, and deep neural networks (DNN), to determine the best predictive solution. The main steps in model building include:

1. **Feature Extraction**: Extract features from game tags, genres, developers, and other relevant data.
2. **Data Processing and Cleaning**: Preprocess features, including normalization and encoding of categorical variables.
3. **Model Selection and Training**: Train several machine learning models and deep learning models (Linear, Polynomial+ridge, XGBoost, DNN) to compare predictive performance.
4. **Model Evaluation and Optimization**: Evaluate models using metrics like RMSE and R-square, and fine-tune them with hyperparameter optimization using Optuna to enhance prediction accuracy.

The ultimate goal is to establish an accurate predictive model that effectively forecasts a game’s first-month sales and provides valuable insights for game developers and marketing strategies.

## References

- **Market Data Sources**: Gamalytic API, Bain & Company Market Reports
- **Technical Documentation**: TF-IDF technical papers, cosine similarity calculation, and more.
