# 주식 데이터가 저장되어 있는 df로부터 각종 다른 지표들을 계산하여 df 의 column에 삽입해주는 함수들
# 지금은 사용 안함
def getMA(df):
    # myprice
    myprice = df['close'] * 0.5 + (df['open'] + df['high'] + df['low'] + df['close']) / 4 * 0.5
    df.insert(len(df.columns), 'myprice', myprice)

    # ma 5/10/20/60/120/250
    ma = df['myprice'].rolling(window=5).mean()
    df.insert(len(df.columns), 'myma5', ma)
    ma = df['myprice'].rolling(window=10).mean()
    df.insert(len(df.columns), 'myma10', ma)
    ma = df['myprice'].rolling(window=20).mean()
    df.insert(len(df.columns), 'myma20', ma)
    ma = df['myprice'].rolling(window=60).mean()
    df.insert(len(df.columns), 'myma60', ma)
    ma = df['myprice'].rolling(window=120).mean()
    df.insert(len(df.columns), 'myma120', ma)
    ma = df['myprice'].rolling(window=250).mean()
    df.insert(len(df.columns), 'myma250', ma)

    # max min
    ma = df['myprice'].rolling(window=120).max()
    df.insert(len(df.columns), 'mymax120', ma)
    ma = df['myprice'].rolling(window=120).min()
    df.insert(len(df.columns), 'mymin120', ma)
    ma = df['myprice'].rolling(window=250).max()
    df.insert(len(df.columns), 'mymax250', ma)
    ma = df['myprice'].rolling(window=250).min()
    df.insert(len(df.columns), 'mymin250', ma)

    # volume mean
    ma = df['volume'].rolling(window=5).mean()
    df.insert(len(df.columns), 'mv5', ma)
    ma = df['volume'].rolling(window=10).mean()
    df.insert(len(df.columns), 'mv10', ma)
    ma = df['volume'].rolling(window=20).mean()
    df.insert(len(df.columns), 'mv20', ma)
    ma = df['volume'].rolling(window=60).mean()
    df.insert(len(df.columns), 'mv60', ma)
    ma = df['volume'].rolling(window=120).mean()
    df.insert(len(df.columns), 'mv120', ma)

    ma = df['volume'].rolling(window=120).std()

    df.set_index('date')