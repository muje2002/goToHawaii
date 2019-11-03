from pattern import basePattern

class sleepWakeReturn(basePattern):
    def __init__(self):
        basePattern.__init__(self)
        self.afterPeriod = 20
        self.Name = "sleepWakeReturn"
        self.prePeriod = 90 + 10 + 15
        # 90일간 조용하다가
        # 5~15일간 상승
        # 10~25일간 침체
        self.count = [0] * 6

    # 받은 df를 기준으로 지금이 pattern이 시작된 날인지 체크
    def isStartPattern(self, df, index):
        # 1. 종가 > 시가 * 1.05 : 4% ~ 10% 양봉이어야 함
        if df.close[index] < df.open[index] * 1.04:# or df.close[index] > df.open[index] * 1.10:
            self.count[0] = self.count[0] + 1
            return False

        # 2. 거래량이 직전 5일평균 1.5배 이상이어야 함
        #if df.volume[index] < df.volume5mean[index-1] * 1.5:
            #return False

        # 3. 직전 40일 중 min과 max가 2이상 차이
        # 상승기간보다 하락기간이 2배 길어야 하며
        # 상승기간은 5일 이상, 하락기간은 10일 이상
        min = df.price[index-40:index].min()
        minidx = df.price[index - 40:index].idxmin()
        max = df.price[index - 40:index].max()
        maxidx = df.price[index - 40:index].idxmax()

        if index < maxidx + 5 or maxidx < minidx + 5 or max < min * 1.8 or index - maxidx < (maxidx - minidx) * 1.2 :
            self.count[1] = self.count[1] + 1
            return False

        # 4. 오늘의 시가가 min - max 의 0.382 부근이어야 함
        if df.open[index] < (max - min) * (0.618 - 0.1) + min or df.open[index] > (max - min) * (0.618 + 0.1) + min:
            self.count[2] = self.count[2] + 1
            return False

        # 5. 상승기간동안 평균 거래량은 전 90일간 평균거래량의 2배 이상이어야 함
        # firstidx = 0 if minidx - 90 < 0 else minidx - 90
        if df.volume[minidx:maxidx+1].mean() < df.volume90mean[minidx - 1] * 2 :
            self.count[3] = self.count[3] + 1
            return False

        # 6. 전 90일간 가격이  min 의 40% 내외여야 함
        firstidx = 0 if minidx - 90 < 0 else minidx - 90
        if df.price[firstidx:minidx].max() > min * (1.0 + 0.4) or df.price[firstidx:minidx].min() < min * (1.0 - 0.4) :
            self.count[4] = self.count[4] + 1
            return False

        # 7. 오늘의 시가가 하락기간동안의 최저가랑 크게 차이가 없어야 함
        if df.open[index] > df.price[maxidx+1:index-1].min() * 1.2 :
            self.count[5] = self.count[5] + 1
            return False

        return True

    # pattern이 시작된 날을 기준으로 몇일 후에 pattern이 종료되는지 (수익/손실을 확정하고 싶은 날
    # getPeriod 기간만큼의 newdf를 받아서 index 날을 기준으로 수익/손실 기록
    def getProfit(self, df, si, li):
        #print("{} -> {}".format(df.price.iloc[0], df.price.iloc[-1]))
        # return (df.price.iloc[-1] * (1 - super().getSlippage()))/ df.price.iloc[0]
        """
        print("next day : {}, last day : {}, peak : {}".\
              format(df.price[si+1]/df.price[si], df.price[li]/df.price[si], df.price[si+1:li+1].max()/df.price[si]))
        """
        #print("{} -> {}, peak {}".format(df.price.iloc[0], df.price.iloc[-1], df[1:].price.max()))
        return (df.price[si + 1:li + 1].mean() * (1 - super().getSlippage() - super().getTax())) / df.price[si]

    def printReturnCount(self):
        for c in self.count :
            print(c)

    def preProcess(self, df):
        #price = df['close'] * 0.5 + (df['open'] + df['high'] + df['low'] + df['close']) / 4 * 0.5
        price = df['close']
        df.insert(len(df.columns), 'price', price)

        v = df['volume'].rolling(window=5).mean()
        df.insert(len(df.columns), 'volume5mean', v)

        v = df['volume'].rolling(window=90).mean()
        df.insert(len(df.columns), 'volume90mean', v)

        df.set_index('date')
