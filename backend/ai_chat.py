import sqlite3
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(question):

    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute("SELECT city, product, price, quantity FROM sales")
    data = cursor.fetchall()

    conn.close()

    context = f"Company sales data: {data}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a business analyst AI."},
            {"role": "user", "content": context + "\n\nQuestion: " + question}
        ]
    )

    return response.choices[0].message.content