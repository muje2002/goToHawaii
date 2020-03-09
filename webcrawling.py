

# 현재 kind.krx.co.kr에 등록된 kospi, kosdaq, konex 종목의 주가데이터(날짜/시고저종/거래량)을 거래시작일부터 모두 가져오는 python code
# naver의 챠트를 count 50000으로 직접 get한 결과를 list -> dataframe -> db 로 저장하는 방식이다.
# 이렇게 하면 수정종가를 가져올 수 있다. 아 빡세..
import pandas as pd
import requests
import sqlite3
from bs4 import BeautifulSoup
import datetime
import environ as env

def getNeed(c, code) :
    # get count : last day ~ today
    q = "SELECT max(date) FROM {tableName} ".format(tableName="A"+code)
    c.execute(q)
    last = c.fetchone()[0]
    now = datetime.datetime.now().date()
    last = datetime.datetime.strptime(last.split()[0],"%Y-%m-%d").date()
    count = now - last

    url = "https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}&requestType=0".format(code=code, count=count)

    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, 'html.parser')
    items = bs_obj.find_all("item")

    for item in items:
        data = item['data'].split("|")

        q = "INSERT INTO {tableName} VALUES ({date}, {open}, {high}, {low}, {close}, {volume})".format(tableName="A"+code,\
            date=datetime.datetime.strptime(data[0],"%Y%m%d").date(), \
            open=int(data[1]),\
            high=int(data[2]),\
            low=int(data[3]),\
            close=int(data[4]),\
            volume=int(data[5]))

        try:
            c.execute(q)
        except sqlite3.Error as e:
            print("Exception in _query: %s" % e)

def getAll(code) :
    count = 5000
    url = "https://fchart.stock.naver.com/sise.nhn?symbol={code}&timeframe=day&count={count}}&requestType=0".format(code=code, count=count)

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
    df.to_sql(name="A"+code, con=stockDB, if_exists='replace', index=False, index_label='date')

    # df.to_csv('D:/__invest__/csv/' + code + '.csv')

if __name__ == "__main__":
    code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

    # 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
    code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

    # 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
    code_df = code_df[['회사명', '종목코드']]
    # 한글로된 컬럼명을 영어로 바꿔준다.
    code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})

    stockDB = sqlite3.connect(env.STOCKDB)
    code_df.to_sql(name="codename", con=stockDB, if_exists='replace', index=False)

    i = 1
    for code in code_df['code']:
        c = stockDB.cursor()
        q = "SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{tableName}'".format(tableName="A" + code)
        c.execute(q)

        # 종가기준이 확 변하면 , getNeed가 아니라 getAll을 호출하는 로직도 필요하겠는데?
        # getNeed가 정상동작을 안하는 것으로 보여서 일단 getAll로 수행
        """
        if c.fetchone()[0] == 1:
            getNeed(c, code)
            print("{0} : {1} get need".format(i, code))
        else:
            """
        getAll(code)
        print("{0} : {1} all".format(i, code))

        i = i + 1

    stockDB.close()