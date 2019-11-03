import pandas_datareader.data as web
import datetime

import matplotlib.pyplot as plt

# 실제로는 2004년 8월 data 부터 존재한다.
start = datetime.datetime(1999, 1, 1)
gs = web.DataReader("078930.KS", "yahoo", start)

print(gs.info())
# 수정종가 반영
plt.plot(gs.index, gs['Adj Close'])
plt.show()