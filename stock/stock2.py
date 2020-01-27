import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.date.today()
stock = web.DataReader("600036.SS", "yahoo", start, end)
change = stock.Close.diff()
change.fillna(change.mean(), inplace=True)
stock['Change'] = change

format = lambda x: '%.2f' % x
stock = stock.applymap(format)

print(stock.head(5))

print(stock.describe())
