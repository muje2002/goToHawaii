from scipy.stats.mstats import gmean
from pattern import basePattern
from scipy import stats as scistats
import environ as env
import util
import numpy as np
import codecs
import pandas as pd

# 보유기간동안 각 날짜까지 수익률을 1일 평균 수익률로 환산(기하평균)
def re1():
    b = basePattern()
    resultpath = env.DBPATH + "bbThrough/1/"
    resultdict = util.load_obj(resultpath + "resultdict")
    date = 60 # afterPeriod 와 동일한 날로 세팅할 것

    total = np.ones((1, date+1))

    for value in resultdict.values():
        v = value['close'].to_numpy()
        v = v.reshape((1, date+1))
        total = np.append(total, v, axis=0)

    newline = []
    for date in range(1, date+1):
        p = []
        for i in range(1, len(total)):  # 1~1353
            p.append((total[i, date] * (1 - b.getSlippage() - b.getTax())) / total[i, 0])

        gm = scistats.gmean(p)
        newline.append("{} : {:.5f}, {:.5f}\n".format(date, gm, gm ** (1 / date)))
        print("{} : {:.5f}, {:.5f}".format(date, gm, gm ** (1 / date)))

    profitJson2 = resultpath + "profit2.json"
    f = open(profitJson2, "w", encoding="utf8")
    for line in newline:
        f.write(line)
    f.close()

# 조건별 전체 결과 (profit.json) 맨 앞에 count 표시
def re2():
    b = basePattern()
    resultpath = env.DBPATH + "bbThrough/"
    profitJson = resultpath + "profit.json"

    f = open(profitJson, "r", encoding="utf8")
    lines = f.readlines()
    newline = []

    for line in lines[2:]:
        folder = line.split()[0].split(".")[0]
        file = folder + "/profit.txt"
        f2 = codecs.open(resultpath + file, "r", encoding="utf8")
        lines2 = f2.readlines()
        count = lines2[4].split()[-1]
        f2.close()
        newline.append(count + " " + line)
    f.close()

    profitJson2 = resultpath + "profit2.json"
    f = open(profitJson2, "w", encoding="utf8")
    for line in newline:
        f.write(line)
    f.close()

# 각 연도별 geomean 구하기
def re3():
    b = basePattern()
    resultpath = env.DBPATH + "bbThrough/1/"
    profitJson = resultpath + "profit.csv"
    df = pd.read_csv(profitJson, usecols=['date', 'profit'], na_values=['1'])

    df['year'] = 0
    for index, row in df.iterrows():
        df['year'].iat[index] = df['date'].iat[index].split('-')[0]
    #print(df)
    print(df.groupby('year').profit.apply(gmean))

    """
    for line in lines[2:]:
        folder = line.split()[0].split(".")[0]
        file = folder + "/profit.txt"
        f2 = codecs.open(resultpath + file, "r", encoding="utf8")
        lines2 = f2.readlines()
        count = lines2[4].split()[-1]
        f2.close()
        newline.append(count + " " + line)
    f.close()

    profitJson2 = resultpath + "profit2.json"
    f = open(profitJson2, "w", encoding="utf8")
    for line in newline:
        f.write(line)
    f.close()
    """

if __name__ == "__main__":
    re1()
    #re2()
    #re3()

    """
    result = np.array(list(resultdict.items()))
    print(result.shape)
    result[][1].to_numpy()
    print(type(result[0][1]))
    """
