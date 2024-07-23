import yfinance as yf

msft=yf.Ticker('MSFT')
#print(msft.info)

history=msft.history('6mo')
print(history)
history.to_csv('msft_stock_data.csv')
