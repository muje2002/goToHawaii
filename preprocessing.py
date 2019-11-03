# pre process total db
import sqlite3
import pandas as pd
import environ as env
import preprocess
from bbThrough import bbThrough

if __name__ == "__main__":
    stockDB = sqlite3.connect(env.STOCKDB)
    preDB = sqlite3.connect(env.PREDB)
    c = stockDB.cursor()

    # get total codes
    q = "SELECT code FROM codename"
    c.execute(q)
    result = c.fetchall()
    codes = [e[0] for e in result]

    pattern = bbThrough()

    i=1
    for code in codes:
        df = pd.read_sql_query("SELECT * FROM {table_name}".format(table_name='A'+code), stockDB)
        df.sort_values(by='date')
        #pre = preprocess.getMA
        pattern.preProcess(df)
        df.to_sql(name="A" + code, con=preDB, if_exists='replace', index=False, index_label='date')
        print(i)
        i=i+1

    stockDB.close()
    preDB.close()