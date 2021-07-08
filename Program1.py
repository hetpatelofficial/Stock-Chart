# Import modules

import fix_yahoo_finance as yf
import pandas as pd
import numpy as np
import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib.transforms as transform
import matplotlib.gridspec as gridspec
import torchvision.transforms as transforms

# Create class for db
class DataBase():
    def __init__(self, ticker, days):
        self.ticker=ticker
        data = yf.download(ticker, start='2020-01-01', end='2021-6-6')
        self.df=pd.DataFrame(data)
        pd.set_option('display.max_columns', None)
        self.df[self.df.index.dayofweek < 5]
        self.df = self.df[-days:]
    def quote(self):
        return self.df



db = DataBase('HDFCBANK.NS',252)
df = db.quote()

print(df.tail())


# Step 4: Adding trend resistance & support lines
pivot_high_1=df['High'][-21:-1].max()
pivot_high_2=df['High'][-55:-22].max()
pivot_low_1=df['Low'][-21:-1].min()
pivot_low_2=df['Low'][-55:-22].min()

A=[df['High'][-21:-1].idxmax(), pivot_high_1]
B=[df['High'][-55:-22].idxmax(), pivot_high_2]

A1=[df['Low'][-21:-1].idxmin(), pivot_low_1]
B1=[df['Low'][-55:-22].idxmin(), pivot_low_2]

x1_high_values = [A[0], B[0]]
y1_high_values = [A[1], B[1]]

x1_low_values = [A1[0], B1[0]]
y1_low_values = [A1[1], B1[1]]



# Step 3: Visualisation with Matplotlib
plt.rcParams.update({'font.size': 10})
fig, ax1 = plt.subplots(figsize=(14,7))

ax1.set_ylabel('Price in ₹')
ax1.set_xlabel('Date')
ax1.set_title('HDFCBANK.NS')
ax1.plot('Adj Close',data=df, label='Close Price', linewidth=0.5, color='blue')

ax1.plot(x1_high_values, y1_high_values, color='g', linestyle='--', linewidth=0.5, label='Trend resistance')
ax1.plot(x1_low_values, y1_low_values, color='r', linestyle='--', linewidth=0.5, label='Trend support')

ax1.axhline(y=pivot_high_1, color='g', linewidth=6, label='First resistance line', alpha=0.2)
ax1.axhline(y=pivot_low_1, color='r', linewidth=6, label='First support line', alpha=0.2)
trans = transform.blended_transform_factory(ax1.get_yticklabels()[0].get_transform(), ax1.transData)
ax1.text(0,pivot_high_1, "{:.2f}".format(pivot_high_1), color="g", transform=trans,ha="right", va="center")
ax1.text(0,pivot_low_1, "{:.2f}".format(pivot_low_1), color="r", transform=trans,ha="right", va="center")

ax1.legend()
ax1.grid()
plt.show()