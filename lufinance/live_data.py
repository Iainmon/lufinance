# __all__ = ['get_current_stock_price', 'get_stock_state_region']
# https://towardsdatascience.com/python-how-to-get-live-market-data-less-than-0-1-second-lag-c85ee280ed93
import yfinance as yf
from yahoo_fin import options
import pandas as pd
import math
import cachetools.func

@cachetools.func.ttl_cache(maxsize=512, ttl=60)
def get_stock_state_region(**kwargs):
    return yf.download(**kwargs)

@cachetools.func.ttl_cache(maxsize=512, ttl=60)
def get_current_stock_price(ticker):
    # data = yf.download(tickers=ticker, period='10m', interval='1m', progress=False)
    data = get_stock_state_region(tickers=ticker, period='10m', interval='1m', progress=False)
    dic = data.to_dict('split')
    average = 0
    averages = {}
    for t in dic['index']:
        key = pd.Timestamp(t)
        openn = data.at[t,'Open']
        close = data.at[t,'Close']
        avg = (openn + close) / 2
        averages[key] = {'average': avg, 'open': openn, 'close': close}
        if dic['index'].index(t) == math.floor(len(dic['index'])/2):
            average = avg
    return average, averages

# a, b = get_current_stock_price('AAPL')
# print(a)