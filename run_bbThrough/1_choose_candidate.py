# 윈도우의 자동프로그램을 이용하여 이 코드가 매일 장 종료후 돌수 있도록 설정하자.
# 이 코드는 다음날 매수할 yyyymmdd_buy_candidate.json을 만들어 낸다.

# yyyymmdd_buy_candidate.json 의 양식
# 종목코드, 종목명, 5일간의 거래량, 249일간 최고가
# name, code, vol_pre_5, pmax_pre_249

# candidate condition
# - 전날 확인 가능한 사항 (조건 3가지)
#   noGoUpFor [5] : 5일간 볼린저밴드 돌파가 일어나지 않았는가? (전날포함)
#   bbwidth [5, 0.04] : 볼린저밴드 width 가 b이하를 a일만큼 유지하였는가 (전날포함)
#   enoughVol [5, 200] : 직전 a일간 거래량이 매일 b이상인가? (전날포함)
#
# - 전날 미리 구해놔야 하는 값들
#   5일간의 평균 거래량 (전날포함)
#   249일간 최고가 (전날포함 249일간 최고가, 당일의 최고가와 MAX하여 250일간 최고가를 구한다)
#     pmax (rolling에 의한 값)은 당일 가격도 포함한다.
#     그러므로 전날 249일치에 대해서 미리 구하고 당일에 최고가와 MAX로 250일간 최고가를 구하는게 유리하다.

import pandas as pd
import requests
import sqlite3
import os
import shutil
import json
from collections import OrderedDict
from datetime import date
from bs4 import BeautifulSoup

STOCKDB = ""
PREDB = ""
DIRPATH = ""
DAYCOUNT = 250

def getAll(code, stockDB) :
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}&requestType=0".format(code=code, count=DAYCOUNT)

    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, 'html.parser')
    items = bs_obj.find_all("item")

    list = []
    for item in items:
        list.insert(0, item['data'].split("|"))

    df = pd.DataFrame(list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    # df.dropna()를 이용해 결측값 있는 행 제거
    df = df.dropna()

    # 데이터의 타입을 int형으로 바꿔줌
    df[['close', 'open', 'high', 'low', 'volume']] = df[['close', 'open', 'high', 'low', 'volume']].astype(int)

    # 컬럼명 'date'의 타입을 date로 바꿔줌
    df['date'] = pd.to_datetime(df['date'])

    # 일자(date)를 기준으로 오름차순 정렬
    df = df.sort_values(by=['date'], ascending=True)
    df.set_index('date')
    preprocess(df)
    df.to_sql(name="A"+code, con=stockDB, if_exists='replace', index=False, index_label='date')

def makeStockDB() :
    global DIRPATH
    global STOCKDB
    global PREDB
    today = date.today().strftime("%Y%m%d")
    DIRPATH = "./db/" + today
    if os.path.exists(DIRPATH) and os.path.isdir(DIRPATH):
        shutil.rmtree(DIRPATH)
    os.makedirs(DIRPATH)
    STOCKDB = DIRPATH + "/stock.db"
    PREDB = DIRPATH + "/pre.db"

    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    code_df = code_df[['회사명', '종목코드']]
    # 한글로된 컬럼명을 영어로 바꿔준다.
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    stockDB = sqlite3.connect(STOCKDB)
    code_df.to_sql(name="codename", con=stockDB, if_exists='replace', index=False)

    i = 1
    for code in code_df['code']:
        getAll(code, stockDB)
        print("{0} : {1} all".format(i, code))
        i = i + 1

    stockDB.close()

def preprocess(df):
    df.set_index('date')
    index = df[df['date'] < "2000-01-01"].index
    df.drop(index, inplace=True)
    df.reset_index(drop=True, inplace=True)

    price = df['close']
    df['price'] = price

    v = df['price'].rolling(window=249).max()
    df['p249max'] = v

    pmean = df['price'].rolling(window=20).mean()
    pstd = df['price'].rolling(window=20).std()

    vhigh = pmean + pstd * 2
    vlow = pmean - pstd * 2
    vbandwidth = (vhigh - vlow) / pmean

    df['vhigh'] = vhigh
    df['vlow'] = vlow
    df['vbandwidth'] = vbandwidth

def makePreDB() :
    #STOCKDB = "./db/20200309/stock.db"
    #PREDB = "./db/20200309/pre.db"
    stockDB = sqlite3.connect(STOCKDB)
    preDB = sqlite3.connect(PREDB)
    c = stockDB.cursor()

    # codename TABLE copy
    df = pd.read_sql_query("SELECT * FROM codename", stockDB)
    df.to_sql(name="codename", con=preDB, if_exists='replace', index=False)

    # get total codes
    q = "SELECT code FROM codename"
    c.execute(q)
    result = c.fetchall()
    codes = [e[0] for e in result]

    i = 1
    for code in codes:
        df = pd.read_sql_query("SELECT * FROM {table_name}".format(table_name='A' + code), stockDB)
        df.sort_values(by='date')
        preprocess(df)
        df.to_sql(name="A" + code, con=preDB, if_exists='replace', index=False, index_label='date')
        print(i)
        i = i + 1

    stockDB.close()
    preDB.close()

#   noGoUpFor [5] : 5일간 볼린저밴드 돌파가 일어나지 않았는가? (전날포함)
#   bbwidth [5, 0.04] : 볼린저밴드 width 가 b이하를 a일만큼 유지하였는가 (전날포함)
#   enoughVol [5, 200] : 직전 a일간 거래량이 매일 b이상인가? (전날포함)
def isCandidate(df, index):
    # 볼린저밴드 width가 0.04이하를 5일간 유지하였는가
    if (df.vbandwidth[index-4 : index+1] <= 0.04).all() == False:
        return False

    # 5일간 거래량이 200 이상인가?
    if (df.volume[index-4 : index+1] > 200).all() == False:
        return False

    # 5일간 볼린저밴드 돌파가 일어나지 않았는가
    for i in range(5):
        if df.open[index-i] < df.vhigh[index-i] and df.close[index-i] > df.vhigh[index-i]:
            return False

    return True

def makeCandidate():
    #PREDB = "./db/20200309/pre.db"
    #DIRPATH = "./db/20200309"
    stockDB = sqlite3.connect(STOCKDB)
    c = stockDB.cursor()

    # get total codes
    q = "SELECT * FROM codename"
    c.execute(q)
    result = c.fetchall()
    names = [e[0] for e in result]
    codes = [e[1] for e in result]

    i=0
    json_list = []
    for code in codes:
        df = pd.read_sql_query("SELECT * FROM {table_name}".format(table_name='A' + code), stockDB)
        df.sort_values(by='date')
        # df의 index는 0부터 시작한다.
        if(len(df) >= DAYCOUNT):
            if (isCandidate(df, len(df)-1) == True):
                print("code:{}, name:{}".format(code, names[i]))
                vol5 = df.volume[len(df)-5 : len(df)].mean()
                json_data = dict()
                json_data["code"] = code
                json_data["name"] = names[i]
                json_data["vol5"] = vol5
                json_data["p249max"] = df.p249max[len(df)-1]
                json_list.append(json_data)

        i = i + 1

    with open(DIRPATH + "/candidate.json", "w", encoding='utf-8') as f:
        json.dump(json_list, f, indent="\t", ensure_ascii=False)

if __name__ == "__main__":
    makeStockDB()
    #makePreDB()
    makeCandidate()