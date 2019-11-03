"""
<1 - 2 정리>
1. yahoo 나 google 에서 df 긁어오기 (file read & write)
2. date index, join, rename 등으로 df 다루기
3. dropna 로 필요없는 row 날리기
4. rox, col 마음대로 slicing 하기
5. normalize 하기
6. plot 으로 graphic 표 확인하기
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
from dateutil.relativedelta import relativedelta
import xlrd
import csv

KOSPI = 'kospi'
KOSDAQ = 'kosdaq'
YAHOO = 'yahoo'
GOOGLE = 'google'

PATH_DATA = "C:\\Users\\ykhong\\PycharmProjects\\Udacity_ML4trading\\data\\"
FILE_SOTCKLIST = {KOSPI:PATH_DATA + "kospilist.txt", KOSDAQ:PATH_DATA + "kosdaqlist.txt"}

def csv_from_excel():
    wb = xlrd.open_workbook('stocklist.xls')
    sh = wb.sheet_by_name('stocklist')
    your_csv_file = open('stocklist.csv', 'wb')
    wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    your_csv_file.close()

def symbol_to_path(symbol, base_dir=""):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))

def read_data(symbols, dates, path):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)

    # drop dates SPY did not trade
    df_temp = pd.read_csv(symbol_to_path(KOSPI, path), index_col='Date',
                          parse_dates=True, usecols=['Date', 'Volume'], na_values=['0'])

    df = df.join(df_temp)
    df = df.dropna(subset=['Volume'])
    df = df.ix[:,[]]

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol, path), index_col='Date',
                              parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['0'])

        df_temp = df_temp.ix[:, ['Adj Close']]
        df_temp = df_temp.rename(columns={'Adj Close': symbol})
        df = df.join(df_temp)

    return df

# run command below in Anaconda console
# $conda install pandas_datareader
import pandas_datareader.data as web
from pathlib import Path

def readFormat(where, type, code):
    if (where == YAHOO) and (type == KOSPI):
        return "{}.KS".format(code)
    if (where == YAHOO) and (type == KOSDAQ):
        return "{}.KS".format(code)
    if (where == GOOGLE) and (type == KOSPI):
        return "KRX:{}".format(code)
    if (where == GOOGLE) and (type == KOSDAQ):
        return "KOSDAQ:{}".format(code)

def get_data(dict, type):
    where = YAHOO

    if not Path(PATH_DATA + "{}.csv".format(KOSPI)).is_file():
        web.DataReader("^KS11", "yahoo").to_csv(PATH_DATA+"{}.csv".format(KOSPI))
    if not Path(PATH_DATA + "{}.csv".format(KOSDAQ)).is_file():
        web.DataReader("^KQ11", "yahoo").to_csv(PATH_DATA + "{}.csv".format(KOSDAQ))
    """
    if not Path(PATH_DATA + "{}.csv".format(KOSPI)).is_file():
        web.DataReader("KRX:KOSPI", GOOGLE).to_csv(PATH_DATA + "{}.csv".format(KOSPI))
    if not Path(PATH_DATA + "{}.csv".format(KOSDAQ)).is_file():
        web.DataReader("KOSDAQ:KOSDAQ", GOOGLE).to_csv(PATH_DATA + "{}.csv".format(KOSDAQ))
    """
    #web.DataReader("078930.KS", "yahoo").to_csv(PATH_DATA + "{0}{1}.csv".format('078930', 'gs'))

    for k, v in dict.items():
        try :
            if not Path(PATH_DATA + "{0}_{1}.csv".format(k, v)).is_file():
                print(readFormat(where, type, k))
                web.DataReader(readFormat(where, type, k), where).to_csv(PATH_DATA + "{0}_{1}.csv".format(k, v))
        except :
            print("error : " + readFormat(where, type, k))
            continue

def normalize_data(df):
    """Normalize stock prices using the first row of the dataframe"""
    return df/df.ix[0,:]

def plot_data(df, title="Stock prices", xlabel="Date", ylabel="Price"):
    """Plot stock prices with a custom title and meaningful axis labels."""
    ax = df.plot(title=title, fontsize=12)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.show()

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start_index:end_index, columns], title="Selected data")

def test_run():
    # Define a date range
    sd = date(2010,1,1)
    ed = date.today()
    dates = pd.date_range(str(sd), str(ed))

    # Choose stock symbols to read
    symbols = ['005930samsung', '036570ncsoft', '078930gs']  # SPY will be added in get_data()

    # Get stock data
    df = read_data(symbols, dates, os.getcwd())
    df = normalize_data(df)
    print(df)

    # Slice and plot
    #plot_selected(df, symbols, sd, ed)
    #plot_selected(df, symbols, str(sd), str(sd+relativedelta(months=+6)))
    plot_selected(df, symbols, str(sd), str(sd + relativedelta(months=+6)))

def get_allstock():
    for k, v in FILE_SOTCKLIST.items():
        names = []
        codes = []
        with open(v) as f:
            for line in f:
                names.append(line.split('\t')[0])
                codes.append(line.split('\t')[1].split('\n')[0])

        stocks = dict(zip(codes,names))
        if k == KOSPI:
            get_data(stocks, k)

if __name__ == "__main__":
    #get_data()
    #test_run()
    get_allstock()
