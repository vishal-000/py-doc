# stock_lstm.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import math
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# ---------- PARAMETERS ----------
TICKER = "AAPL"                  # change to any ticker (e.g., 'TSLA', 'INFY.NS')
START_DATE = "2015-01-01"
END_DATE = None                   # None -> up to today
SEQUENCE_LENGTH = 60              # number of past days used to predict next day
TEST_SPLIT = 0.2
BATCH_SIZE = 32
EPOCHS = 50
MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

# ---------- 1. Download data ----------
def download_data(ticker, start, end=None):
    df = yf.download(ticker, start=start, end=end)
    if df.empty:
        raise ValueError("No data downloaded. Check ticker and dates.")
    return df

print("Downloading data...")
df = download_data(TICKER, START_DATE, END_DATE)
print(f"Downloaded {len(df)} rows from {df.index.min().date()} to {df.index.max().date()}")

# ---------- 2. Exploratory (optional) ----------
plt.figure(figsize=(12,6))
plt.plot(df['Close'], label='Close Price')
plt.title(f"{TICKER} Close Price")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.show()

# ---------- 3. Use 'Close' price and scale ----------
data_close = df[['Close']].copy()
scaler = MinMaxScaler(feature_range=(0, 1))
scaled = scaler.fit_transform(data_close.values)  # shape (n,1)

# ---------- 4. Create sequences ----------
def create_sequences(data, seq_length):
    X, y = [], []
    for i in range(seq_length, len(data)):
        X.append(data[i-seq_length:i, 0])
        y.append(data[i, 0])
    X, y = np.array(X), np.array(y)
    # reshape for LSTM [samples, timesteps, features]
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))
    return X, y

X, y = create_sequences(scaled, SEQUENCE_LENGTH)
print("Total sequences:", X.shape[0])

# ---------- 5. Train/test split ----------
split_idx = int(X.shape[0] * (1 - TEST_SPLIT))
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

print("Train sequences:", X_train.shape[0], "Test sequences:", X_test.shape[0])

# ---------- 6. Build LSTM model ----------
def build_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50, return_sequences=False),
        Dropout(0.2),
        Dense(25),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

model = build_model((X_train.shape[1], 1))
model.summary()

# ---------- 7. Callbacks ----------
checkpoint_path = os.path.join(MODEL_DIR, f"{TICKER}_best.h5")
callbacks = [
    EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
    ModelCheckpoint(checkpoint_path, monitor='val_loss', save_best_only=True)
]

# ---------- 8. Train ----------
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=EPOCHS,
    batch_size=BATCH_SIZE,
    callbacks=callbacks,
    verbose=1
)

# plot training & validation loss
plt.figure(figsize=(8,4))
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.show()

# ---------- 9. Predict ----------
predictions = model.predict(X_test)
# invert scaling
predictions_unscaled = scaler.inverse_transform(predictions)
y_test_unscaled = scaler.inverse_transform(y_test.reshape(-1,1))

# compute RMSE
rmse = math.sqrt(mean_squared_error(y_test_unscaled, predictions_unscaled))
print(f"Test RMSE: {rmse:.4f}")

# ---------- 10. Visualize predictions vs actual ----------
# Build a dataframe for plotting aligned with original dates
test_start_idx = len(data_close) - len(y_test_unscaled)
plot_df = data_close.copy().reset_index()
plot_df['Predicted'] = np.nan

pred_len = len(predictions_unscaled)
plot_df.loc[len(plot_df) - pred_len:, 'Predicted'] = predictions_unscaled.flatten()

plt.figure(figsize=(14,6))
plt.plot(plot_df['Date'], plot_df['Close'], label='Actual Close')
plt.plot(plot_df['Date'], plot_df['Predicted'], label='Predicted Close')
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(f"{TICKER} Actual vs Predicted Close Price")
plt.legend()
plt.show()
