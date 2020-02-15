# 상승 패턴 알고리즘 "bbThrough"
from pattern import basePattern
import matplotlib.pyplot as plt
import pylab as pl

class bbThrough(basePattern):
    def __init__(self):
        basePattern.__init__(self)
        self.afterPeriod = 39
        self.Name = "bbThrough"
        self.prePeriod = 250
        self.SHOW = False
        self.condition = {}

    def getCondition(self):
        return self.condition

    def setCondition(self, condition):
        self.condition = condition
        if 'afterPeriod' in self.condition:
            ap = self.condition['afterPeriod']
            self.afterPeriod = ap
            print('afterPeriod : {}'.format(ap))

    # 받은 df를 기준으로 지금이 pattern이 시작된 날인지 체크
    def isStartPattern(self, df, index):

        # 오늘 볼린저 밴드를 돌파하였는가
        if 'goThrough' in self.condition and self.condition['goThrough'] == True:
            if df.open[index] >= df.vhigh[index] or df.close[index] <= df.vhigh[index]:
                return False

        # 양봉인가
        if 'goUp' in self.condition and self.condition['goUp'] == True:
            if df.open[index] >= df.close[index]:
                return False

        # 250일간 최고가에서 b%이상 떨어지지 않았는가?
        if 'nearHigh' in self.condition:
            # if df.price[index] > df.p250max[index] * (1 + 0.1) or df.price[index] < df.p250max[index] * (1 - 0.1):
            clist = self.condition['nearHigh']
            for day, up, down in clist:
                #print('nearHigh : {} {}'.format(up, down))
                if day == 250 :
                    if df.price[index] > df.p250max[index] * up or df.price[index] < df.p250max[index] * down:
                        return False
                elif day == 120:
                    if df.price[index] > df.p120max[index] * up or df.price[index] < df.p120max[index] * down:
                        return False
                else :
                    if df.price[index] > df.price[index-day : index].max() * up or df.price[index] < df.price[index-day : index].max() * down:
                        return False

        # 볼린저밴드 width가 10%이하를 20일간 유지하였는가
        if 'bbwidth' in self.condition:
            clist = self.condition['bbwidth']
            # day 20, width 0.1, day 5, width 0.5
            for day, width in clist:
                #print('bbwidth : {} {}'.format(day, width))
                if (df.vbandwidth[index - day:index] <= width).all() == False:
                    return False

        # 5일간 거래량이 200 이상인가?
        if 'enoughVol' in self.condition:
            clist = self.condition['enoughVol']
            for day, vol in clist:
                #print('enoughVol : {} {}'.format(day, vol))
                if (df.volume[index - day:index] > vol).all() == False:
                    return False

        if 'enoughTodayVol' in self.condition:
            clist = self.condition['enoughTodayVol']
            for day, rate in clist:
                if df.volume[index] < df.volume[index-day : index].mean() * rate :
                    return False

        # 5일간 볼린저밴드 돌파가 일어나지 않았는가
        if 'noGoUpFor' in self.condition:
            day = self.condition['noGoUpFor']
            #print('noGoUpFor : {}'.format(day))
            for i in range(day):
                if df.open[index - i - 1] < df.vhigh[index - i - 1] and df.close[index - i - 1] > df.vhigh[index - i - 1]:
                    return False

        # 거래대금이 1억이하면 구매하지 않음
        if 'totalPrice' in self.condition:
            _totalPrice = self.condition['totalPrice']
            if _totalPrice > df.volume[index] * df.price[index] :
                return False
        """
        # 1. 볼린저밴드 상단 근접 3% 이내를 3일간 유지하였는가?
        df1 = df.price[index - 2:index + 1] >= df.vhigh[index - 2:index + 1] * 0.97
        df2 = df.price[index - 2:index + 1] <= df.vhigh[index - 2:index + 1]
        if df1.all() == False or df2.all() == False :
            return False
        """

        return True

    def getProfit(self, df, si, li):
        """
        #10일전에 10%면 매도
        p = df.iloc[si:si + 11]
        p = p.loc[(p['price'] / p['price'][si]) <= 0.9]

        if p.empty == False:
            return (p.price.iloc[0] * (1 - self.getSlippage() - self.getTax())) / df.price[si]

        # 20일전에 20%면 매도
        p = df.iloc[si:si + 21]
        p = p.loc[(p['price'] / p['price'][si]) <= 0.8]

        if p.empty == False:
            return (p.price.iloc[0] * (1 - self.getSlippage() - self.getTax())) / df.price[si]

        # 30일에 매도
        return super().getLast(df, si, li)
        """

        return super().getLast(df, si, li)

        # 전략 1. 볼린저밴드 하단 선을 아래로 돌파하면 그날 종가로 매도한다. 에이 안좋네
        """
        p = df.iloc[si:li+1]
        p = p.loc[p['close'] < p['vlow']]

        if p.empty == True:
            return super().getLast(df, si, li)
        else:
            return (p.close.iloc[0] * (1 - self.getSlippage() - self.getTax())) / df.price[si]
        """

    def getAll(self, df, si, li):
        return df[si:li+1]

    def preProcess(self, df):
        #price = df['close'] * 0.5 + (df['open'] + df['high'] + df['low']) / 3 * 0.5
        df.set_index('date')
        index = df[df['date'] < "2000-01-01"].index
        df.drop(index, inplace=True)
        df.reset_index(drop=True, inplace=True)
        #print(df)

        price = df['close']
        df['price'] = price
        #df.insert(len(df.columns), 'price', price)

        v = df['price'].rolling(window=250).max()
        df['p250max'] = v

        v = df['price'].rolling(window=120).max()
        df['p120max'] = v

        pmean60 = df['price'].rolling(window=60).mean()
        pmean = df['price'].rolling(window=20).mean()
        pstd = df['price'].rolling(window=20).std()

        vhigh = pmean + pstd * 2
        vlow = pmean - pstd * 2
        vbandwidth = (vhigh - vlow) / pmean

        df['pmean60'] = pmean60
        df['vhigh'] = vhigh
        df['vlow'] = vlow
        df['vbandwidth'] = vbandwidth

    def showGraph(self, code, df, p, i, n, prof):
        if(self.SHOW == False):
            return

        newdf = df[p:n]
        i = i - p

        pl.rcParams["figure.figsize"] = (30, 15)
        pl.rcParams['axes.grid'] = True

        fig = pl.figure()
        priceplot = pl.subplot2grid((5, 3), (0, 0), fig=fig, rowspan=3, colspan=3)
        priceplot.plot(newdf['date'], newdf['price'], label='price')
        priceplot.plot(newdf['date'], newdf['vhigh'], 'g', label='vhigh')
        priceplot.plot(newdf['date'], newdf['vlow'], 'g', label='vlow')
        priceplot.axvline(x=newdf['date'].iloc[i], color='r', linestyle='-', linewidth=1)

        widthplot = pl.subplot2grid((5, 3), (3, 0), rowspan=1, colspan=3)
        #widthplot.get_yaxis().get_major_formatter().set_scientific(False)
        widthplot.plot(newdf['date'], newdf['vbandwidth'])
        widthplot.axvline(x=newdf['date'].iloc[i], color='r', linestyle='-', linewidth=1)

        vplot = pl.subplot2grid((5, 3), (4, 0), rowspan=1, colspan=3)
        # bottom_axes.get_yaxis().get_major_formatter().set_scientific(False)
        vplot.plot(newdf['date'], newdf['volume'])
        vplot.axvline(x=newdf['date'].iloc[i], color='r', linestyle='-', linewidth=1)

        #pl.tight_layout()
        pl.grid()
        if prof > 1.0 :
            filename = self.dirpath + "prof/" + "{:.4f}".format(prof) + "_" + code + "_" + df['date'].iloc[i][:10] + ".png"
        else:
            filename = self.dirpath + "loss/" + "{:.4f}".format(prof) + "_" + code + "_" + df['date'].iloc[i][:10] + ".png"
        fig.savefig(filename, format='png')
        fig.clf()
        pl.clf()
        pl.close(fig)
