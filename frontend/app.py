import streamlit as st
import requests
import matplotlib.pyplot as plt

st.title("AstraMind Dashboard 🚀")

# Backend URL
BASE_URL = "http://127.0.0.1:8000"

# Revenue Button
if st.button("Show Total Revenue"):
    response = requests.get(f"{BASE_URL}/revenue")
    data = response.json()
    st.write("Total Revenue:", data["total_revenue"])

# Forecast Button
if st.button("Show 30 Day Forecast"):
    response = requests.get(f"{BASE_URL}/forecast")
    data = response.json()

    forecast = data["next_30_days_forecast"]

    plt.figure()
    plt.plot(forecast)
    plt.xlabel("Days")
    plt.ylabel("Predicted Revenue")

    st.pyplot(plt)