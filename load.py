import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Nifty.csv')
data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y %H:%M')
data['Month'] = data['Date'].dt.to_period('M')

def calculate_vwap(group):
    total_value = (group['Close'] * group['Volume']).cumsum()
    total_volume = group['Volume'].cumsum()
    return total_value / total_volume

def calculate_high_low(group):
    group['Highest High'] = group['High'].cummax()
    group['Lowest Low'] = group['Low'].cummin()
    return group

data['VWAP'] = data.groupby('Month').apply(calculate_vwap).reset_index(level=0, drop=True)
data = data.groupby('Month').apply(calculate_high_low).reset_index(drop=True)

plt.figure(figsize=(14, 7))
plt.plot(data['Date'], data['Close'], label='Close Price', color='blue')
plt.plot(data['Date'], data['VWAP'], label='VWAP', color='green', linestyle='--')
plt.plot(data['Date'], data['Highest High'], label='Highest High', color='red', linestyle='--')
plt.plot(data['Date'], data['Lowest Low'], label='Lowest Low', color='orange', linestyle='--')
plt.title('Closing Price, VWAP, Highest High, and Lowest Low')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
