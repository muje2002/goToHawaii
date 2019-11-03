import time
import operator
from os import listdir
from os.path import isfile, join
import shutil
import json
import sqlite3
import os
import pandas as pd
import environ as env
import util
from bbThrough import bbThrough
from Profit import Profit

resultNum = 3

def simulate(df, p, code):
    prePeriod = p.getPrePeriod()
    afterPeriod = p.getAfterPeriod()

    #_profit = [[] for i in range(resultNum)]
    i=0
    nextIndex = -1
    for index, row in df.iterrows():
        # index는 0부터 시작한다

        # pattern 다음의 기간으로 index를 이동
        if(index < nextIndex) :
            continue

        # prePeriod 기간 이전의 index면 continue
        if(index < prePeriod):
            continue

        if(index >= len(df) - afterPeriod):
            break

        if(p.isStartPattern(df, index) == True) :
            nextIndex = index + afterPeriod
            if nextIndex >= len(df) :
                nextIndex = len(df) - 1

            prof = p.getProfit(df, index, nextIndex)
            p_profit.add(code, df.date[index], prof)
            p_last.add(code, df.date[index], p.getLast(df, index, nextIndex))
            p_mean.add(code, df.date[index], p.getMean(df, index, nextIndex))

            rdf = p.getAll(df, index, nextIndex)
            resultdict[code + " " + rdf.date.iloc[0]] = rdf

            if prof >= 1.0 :
                p.showGraph(code, df, index-prePeriod, index, nextIndex, prof)
            else :
                p.showGraph(code, df, index - prePeriod, index, nextIndex, prof)

            i = i + 1

    return i

if __name__ == "__main__":

    # get total codes
    stockDB = sqlite3.connect(env.PREDB)
    c = stockDB.cursor()
    q = "SELECT name FROM sqlite_master WHERE type='table';"
    c.execute(q)
    result = c.fetchall()
    codes = [e[0] for e in result]

    # pattern
    pattern = bbThrough()

    mypath = env.DBPATH + pattern.getName() + "/"
    jFileNameList = [f for f in listdir(mypath) if isfile(join(mypath, f)) and f.split('.')[-1] == 'json']

    maxProfit = 0
    profitDict={}
    j=0

    for jFileName in jFileNameList :
        start = time.time()
        jsonFile = mypath + jFileName
        with open(jsonFile) as jf:
            condition = json.load(jf)
            pattern.setCondition(condition)

        # Profit
        p_profit = Profit("profit")
        p_last = Profit("last")
        p_mean = Profit("mean")

        # set result Path
        #util.makeFolder(pattern.getName())
        resultpath = util.makeFolder(pattern.getName()+"/" +jFileName.split('.')[0]+"/")
        os.makedirs(resultpath + "prof/")
        os.makedirs(resultpath + "loss/")
        p_profit.setPath(resultpath)
        p_last.setPath(resultpath)
        p_mean.setPath(resultpath)
        pattern.setPath(resultpath)
        shutil.copyfile(jsonFile, resultpath+jFileName)

        resultdict = {}

        i=1
        totalCount = 0
        for code in codes: # 모든 종목에 대해서
            df = pd.read_sql_query("SELECT * FROM {table_name}".format(table_name=code), stockDB)
            df.sort_values(by='date')
            # 분석전에 필요한 지표가 있으면 미리 뽑는다.
            #pattern.preProcess(df)
            # 해당 종목 (df)가 해당 패턴인지 갯수를 센다.
            count = simulate(df, pattern, code)
            totalCount = totalCount + count
            print("{}: code[{}] {} discovered, total {}".format(i, code, count, totalCount))
            #p_profit.printGmean()
            i=i+1

        util.save_obj(resultdict, resultpath + "resultdict")
        #hi = util.load_obj(resultpath + "resultdict")

        condition = pattern.getCondition()
        patternMatchCnt = p_profit.printProfit(condition)
        p_profit.saveFile()
        p_profit.drawCountPerProfit()

        p_last.printProfit(condition)
        p_last.saveFile()

        p_mean.printProfit(condition)
        p_mean.saveFile()

        tempp = p_profit.printGmean()
        profitPerDay = tempp ** (1/pattern.afterPeriod)
        #pperday = {'pperday': profitPerDay}
        condition['profit'] = tempp
        condition['pperday'] = profitPerDay
        condition['count'] = patternMatchCnt
        profitDict[jFileName] = condition

        if(profitPerDay > maxProfit) :
            maxProfit = profitPerDay
            print("maxProfit : {} / 1 day".format(profitPerDay))
            print("condition : {}".format(jFileName))
        j=j+1
        print("{} complete, {} sec used".format(j, time.time() - start))

    sorted_x = sorted(profitDict.items(), key=lambda kv : kv[1]['pperday'])
    sorted_x = sorted_x[::-1]
    vsorted_x = "\n".join("{}\t{}".format(k, v.values()) for k, v in sorted_x)
    ksorted_x = "filename\t{}\n".format(sorted_x[0][1].keys())

    #j = json.dumps(psorted_x)
    f = open("{}{}.json".format(mypath, "profit"), "w")
    f.write(ksorted_x)
    f.write('\n')
    f.write(vsorted_x)
    f.close()

    stockDB.close()