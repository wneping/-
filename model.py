import pandas as pd
from sklearn.ensemble import RandomForestRegressor


CSV_PATH = r"C:/Users/b8002/Desktop/stock_predict/day0222.csv"


def load_data():

    df = pd.read_csv(CSV_PATH)

    df['日期'] = pd.to_datetime(df['日期'])

    df = df.sort_values("日期")

    # 移除逗號
    numeric_columns = [
        "成交股數",
        "成交金額",
        "開盤價",
        "最高價",
        "最低價",
        "收盤價",
        "成交筆數"
    ]

    for col in numeric_columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "")
            .str.replace("+", "")
            .str.replace("--", "")
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 刪除 NaN
    df = df.dropna()

    return df



def train_model(df):

    features = [
        "開盤價",
        "最高價",
        "最低價",
        "成交股數",
        "成交金額",
        "成交筆數"
    ]

    X = df[features]

    y = df["收盤價"]

    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42
    )

    model.fit(X, y)

    return model



def predict_next(model, df):

    last = df.iloc[-1:]

    X_last = last[
        [
            "開盤價",
            "最高價",
            "最低價",
            "成交股數",
            "成交金額",
            "成交筆數"
        ]
    ]

    prediction = model.predict(X_last)

    return prediction[0]