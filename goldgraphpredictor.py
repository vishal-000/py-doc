# gold_price_predictor.py
# -----------------------------------------------
# 📊 Indian Gold Price Predictor (GOLDBEES.NS)
# Using Linear Regression on Yahoo Finance Data
# -----------------------------------------------

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Step 1: Fetch gold ETF data (GOLDBEES.NS)
print("Fetching gold data from Yahoo Finance...")
data = yf.download("GOLDBEES.NS", start="2015-01-01", end="2025-01-01")

# Step 2: Keep only closing price
data = data[['Close']]
data.dropna(inplace=True)

# Step 3: Create a prediction column (shifted 30 days ahead)
forecast_out = 30  # predict 30 days into the future
data['Prediction'] = data[['Close']].shift(-forecast_out)

# Step 4: Create features (X) and target (y)
X = np.array(data.drop(['Prediction'], axis=1))[:-forecast_out]
y = np.array(data['Prediction'])[:-forecast_out]

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Step 6: Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 7: Check model accuracy
acc = model.score(X_test, y_test)
print(f"✅ Model Accuracy: {acc*100:.2f}%")

# Step 8: Predict the next 30 days
x_future = np.array(data.drop(['Prediction'], axis=1))[-forecast_out:]
predictions = model.predict(x_future)

# Step 9: Visualize the predictions
valid = data[-forecast_out:].copy()
valid['Predictions'] = predictions

plt.figure(figsize=(12, 6))
plt.title("Indian Gold Price Prediction (GOLDBEES.NS)", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Price (INR)", fontsize=12)
plt.plot(data['Close'], label="Actual Price", color='blue')
plt.plot(valid['Predictions'], label="Predicted Price (Next 30 days)", color='orange')
plt.legend()
plt.grid(True)
plt.show()

# Step 10: Print predicted prices
print("\n📅 Predicted Gold Prices for Next 30 Days:")
print(valid[['Predictions']])
