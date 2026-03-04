import sqlite3
import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model():
    conn = sqlite3.connect("sales.db")
    
    df = pd.read_sql_query("SELECT price, quantity FROM sales", conn)
    
    conn.close()

    # Revenue column बनाओ
    df["revenue"] = df["price"] * df["quantity"]

    X = df[["price", "quantity"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    return model


import numpy as np

def train_time_series():
    conn = sqlite3.connect("sales.db")
    
    df = pd.read_sql_query("SELECT date, price, quantity FROM sales", conn)
    
    conn.close()

    df["revenue"] = df["price"] * df["quantity"]

    # Date को number में convert करो
    df["date"] = pd.to_datetime(df["date"])
    df["day_number"] = (df["date"] - df["date"].min()).dt.days

    X = df[["day_number"]]
    y = df["revenue"]

    model = LinearRegression()
    model.fit(X, y)

    return model, df["day_number"].max()