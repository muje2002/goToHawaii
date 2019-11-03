import pandas_datareader.data as web
import datetime

start = datetime.datetime(1985, 1, 1)
end = datetime.datetime(2019, 8, 30)
#gs = web.DataReader("000020.KS", "yahoo", start, end)
web.DataReader("000020.KS", "yahoo").to_csv("D:/__invest__/db/" + "{0}.csv".format('000020'))

