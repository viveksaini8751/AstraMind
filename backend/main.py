
from fastapi import FastAPI
from .database import create_table
from backend.database import create_table, insert_sample_data

create_table()
insert_sample_data()





app = FastAPI()

@app.get("/")
def home():
    return {"message": "AstraMind is starting 🚀"}


import sqlite3

@app.get("/sales")
def get_sales():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sales")
    rows = cursor.fetchall()

    conn.close()

    return {"data": rows}

@app.get("/test-db")
def test_db():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return {"tables": tables}


@app.get("/revenue")
def calculate_revenue():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT price, quantity FROM sales")
    rows = cursor.fetchall()

    total_revenue = 0

    for row in rows:
        price = row[0]
        quantity = row[1]
        total_revenue += price * quantity

    conn.close()

    return {"total_revenue": total_revenue}


@app.get("/city-revenue")
def city_revenue():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT city, SUM(price * quantity) 
        FROM sales
        GROUP BY city
    """)

    rows = cursor.fetchall()

    conn.close()

    return {"city_revenue": rows}


@app.get("/profit")
def calculate_profit():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT price, quantity FROM sales")
    rows = cursor.fetchall()

    total_profit = 0

    for row in rows:
        price = row[0]
        quantity = row[1]

        cost = price * 0.7
        profit = (price - cost) * quantity

        total_profit += profit

    conn.close()

    return {"total_profit": total_profit}


@app.get("/top-product")
def top_product():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product, SUM(quantity) as total_quantity
        FROM sales
        GROUP BY product
        ORDER BY total_quantity DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return {"top_product": row}

@app.get("/loss-products")
def loss_products():
    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT product, price, quantity FROM sales")
    rows = cursor.fetchall()

    loss_list = []

    for row in rows:
        product = row[0]
        price = row[1]
        quantity = row[2]

        cost = price * 1.1  # मान लो cost ज्यादा है
        profit = (price - cost) * quantity

        if profit < 0:
            loss_list.append(product)

    conn.close()

    return {"loss_products": loss_list}


from backend.ml_model import train_model

model = train_model()

@app.get("/predict")
def predict(price: float, quantity: int):
    prediction = model.predict([[price, quantity]])
    return {"predicted_revenue": float(prediction[0])}



from backend.ml_model import train_time_series
import numpy as np

ts_model, last_day = train_time_series()

@app.get("/forecast")
def forecast():
    future_days = np.array([[last_day + i] for i in range(1, 31)])
    predictions = ts_model.predict(future_days)

    result = predictions.tolist()

    return {"next_30_days_forecast": result}

from backend.ai_chat import ask_ai

@app.get("/chat")
def chat(question: str):
    answer = ask_ai(question)
    return {"answer": answer}