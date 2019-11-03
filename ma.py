import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt

# 실제로는 2004년 8월 data 부터 존재한다.
start = datetime.datetime(1999, 1, 1)
gs = web.DataReader("078930.KS", "yahoo", start)

# 거래량이 0인 날 제외
new_gs = gs[gs['Volume'] !=0]

ma20 = new_gs['Adj Close'].rolling(window=20).mean()
ma60 = new_gs['Adj Close'].rolling(window=60).mean()
ma120 = new_gs['Adj Close'].rolling(window=120).mean()
new_gs.insert(len(new_gs.columns), "MA20", ma20)
new_gs.insert(len(new_gs.columns), "MA60", ma60)
new_gs.insert(len(new_gs.columns), "MA120", ma120)

plt.plot(new_gs.index, new_gs['Adj Close'], label="Adj Close")
plt.plot(new_gs.index, new_gs['MA20'], label="MA20")
plt.plot(new_gs.index, new_gs['MA60'], label="MA60")
plt.plot(new_gs.index, new_gs['MA120'], label="MA120")

plt.legend(loc='best')
plt.grid()

plt.show()