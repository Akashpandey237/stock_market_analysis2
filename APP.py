import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from keras.models import load_model
import streamlit as st
import yfinance as yf
import datetime

# Define the path to your Keras model
model_path = 'C:/Users/akash pandey/stock_market_analysis/stock_market_analysis/stock_market_analysis/keras_model.h5'

# Load the Keras model
model = load_model(model_path)

# Define the date range for stock data
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2019, 12, 31)

# Streamlit app title
st.title('Stock Trend Prediction')

# User input for stock ticker symbol
user_input = st.text_input('Enter Stock Ticker', 'AAPL')

# Download stock data from Yahoo Finance
df = yf.download(user_input, start=start, end=end)

# Display data summary
st.subheader('Data from 2010 - 2019')
st.write(df.describe())

# Visualize closing price vs. time
st.subheader('Closing Price vs Time chart')
fig = plt.figure(figsize=(12, 6))
plt.plot(df.Close)
st.pyplot(fig)

# Visualize closing price vs. time with 100-day moving average
ma100 = df.Close.rolling(100).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)

# Visualize closing price vs. time with 100-day and 200-day moving averages
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig = plt.figure(figsize=(12, 6))
plt.plot(ma100, 'r')
plt.plot(ma200, 'g')
plt.plot(df.Close, 'b')
st.pyplot(fig)

# Splitting Data into Training and Testing
data_training = pd.DataFrame(df['Close'][0:int(len(df) * 0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df) * 0.70):int(len(df))])

# Data scaling
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler(feature_range=(0, 1))
data_training_array = scaler.fit_transform(data_training)

# Testing part
past_100_days = data_training.tail(100)
final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test = []
y_test = []

for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i - 100:i])
    y_test.append(input_data[i, 0])

x_test, y_test = np.array(x_test), np.array(y_test)
y_predicted = model.predict(x_test)

scaler = scaler.scale_
scale_factor = 1 / scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

# Final Graph
# Flatten y_predicted to make it 2D (if it contains multiple time steps)
y_predicted = y_predicted.reshape(-1, 1)

# Create a figure object
fig2 = plt.figure(figsize=(10, 6))

# Plot the original and predicted data on the figure
plt.plot(y_test, 'b', label='original price')
plt.plot(y_predicted, 'r', label='predicted price')
plt.xlabel('time')
plt.ylabel('price')
plt.legend()

# Save the figure
fig2.savefig('plot.png')

# Display the figure in Streamlit
st.image('plot.png')
