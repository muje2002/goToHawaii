import os
class basePattern:
    def __init__(self):
        self.afterPeriod = 0
        self.prePeriod = 0
        self.Name = ""
        self.SLIPPAGE = 0.001
        self.TAX = 0.0033
        self.dirpath = ""
        self.SHOW = False

    def getName(self):
        return self.Name

    def getPrePeriod(self):
        return self.prePeriod

    # 받은 df를 기준으로 지금이 pattern이 시작된 날인지 체크
    def isStartPattern(self, df):
        return True

    # pattern이 시작된 날을 기준으로 몇일 후에 pattern이 종료되는지 (수익/손실을 확정하고 싶은 날
    def getAfterPeriod(self):
        return self.afterPeriod

    # getPeriod 기간만큼의 newdf를 받아서 index 날을 기준으로 수익/손실 기록
    def getProfit(self, newdf):
        return 1

    def preProcess(self, df):
        pass

    def getSlippage(self):
        return self.SLIPPAGE

    def getTax(self):
        return self.TAX

    def getMean(self, df, si, li):
        return (df.price[si + 1:li + 1].mean() * (1 - self.getSlippage() - self.getTax())) / df.price[si]

    def getMax(self, df, si, li):
        return (df.price[si + 1:li + 1].max() * (1 - self.getSlippage() - self.getTax())) / df.price[si]

    def getLast(self, df, si, li):
        return (df.price[li] * (1 - self.getSlippage() - self.getTax())) / df.price[si]

    def setPath(self, path):
        if os.path.exists(path) == False:
            os.makedirs(path)
        self.dirpath = path