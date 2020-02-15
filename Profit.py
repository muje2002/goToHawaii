from scipy.stats.mstats import gmean
import numpy as np
import environ as env
import codecs
from itertools import chain
import os
import shutil
import pandas as pd
import pylab as pl
import json

class Profit:
    def __init__(self, name):
        self.dirpath = ""
        self.name = name
        self.profitlist = pd.DataFrame(columns=["code", "date", "profit"])

    def printGmean(self):
        if(self.profitlist.size == 0):
            return 1
        print("{}, {:.4f}".format(self.profitlist['profit'].count(), gmean(self.profitlist['profit'].to_numpy())))
        return gmean(self.profitlist['profit'].to_numpy())

    def printEach(self, p, f):
        # count
        f.write("\t횟수 : {}\n".format(p.size))

        if(p.size == 0):
            return

        p = p.flatten()
        # max profit
        f.write("\t최대 : {}\n".format(p.max()))

        # min profit
        f.write("\t최소 : {}\n".format(p.min()))

        # 산술평균
        f.write("\t산술평균 : {}\n".format(p.mean()))

        # 기하평균
        f.write("\t기하평균 : {}\n".format(gmean(p)))
        f.write("\n")

    def add(self, code, date, profit):
        a = pd.DataFrame(data=[[code, date, profit]], columns=["code", "date", "profit"])
        self.profitlist = self.profitlist.append(a)

    def printProfit(self, condition):
        filename = self.dirpath + self.name + ".txt"
        f = codecs.open(filename, "a", encoding="utf8")
        f.write("===== {} =====\n\n".format(self.name))
        f.write(json.dumps(condition))
        f.write("\n")

        #total = list(chain.from_iterable(self.profitlist))
        #total = np.array(self.profitlist.profit.to_)
        total = self.profitlist['profit'].to_numpy()

        f.write("[합계]\n")
        self.printEach(total, f)

        prof = total[np.where(total > 1)]
        loss = total[np.where(total < 1)]

        if len(total) != 0 :
            f.write("[승률] {}\n\n".format(len(prof)/len(total)))
        """
        f.write("[이익]\n")
        self.printEach(prof, f)

        f.write("[손실]\n")
        self.printEach(loss, f)
        """

        #dates = self.profitlist['date'].to_numpy()
        sorted = self.profitlist.sort_values(["date"], ascending=[False])
        sorted_year = sorted['date'].str.split('-').str[0]
        sorted['sorted_year'] = sorted_year
        mean = sorted.groupby('sorted_year').mean()
        count = sorted.groupby('sorted_year').count()
        mean['count'] = count['profit']

        f.write("[연도별] \n")
        f.write(mean.to_string())
        """
        for index, row in mean.iterrows():
            f.write("{} count:{}\tpro:{}\n".format(index, row.count, row.profit))

        
        year, count = np.unique(sorted_year, return_counts=True)
        for y, c in list(zip(year, count)):
            f.write("{}:{}\n".format(y, c))
        """

        f.close()
        return total.size

    def setPath(self, path):
        self.dirpath = path

    def saveFile(self):
        sorted = self.profitlist.sort_values(["profit"], ascending=[True])
        filename = self.dirpath + self.name + ".csv"
        sorted.to_csv(filename, mode='w')
        return

    def loadFile(self, filename):
        self.profitlist = pd.read_csv(filename)
        return

    def drawCountPerProfit(self):
        sorted = self.profitlist.sort_values(["profit"], ascending=[True])
        # 3배 이상이면 drop
        sorted.drop(sorted[sorted['profit'] >= 3].index, inplace=True)

        sorted['profit'] = sorted['profit'] * 20
        profint = sorted['profit'].astype(int) * 5

        prof, count = np.unique(profint, return_counts=True)

        pl.rcParams["figure.figsize"] = (30, 15)
        pl.rcParams['axes.grid'] = True

        fig = pl.figure()
        pl.bar(prof, count)
        pl.xticks(np.arange(0, 300, step=5))
        #pl.yticks(np.arange(0, 50, step=5))

        filename = self.dirpath + self.name + ".png"
        fig.savefig(filename, format='png')
        fig.clf()
        pl.close(fig)