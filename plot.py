import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

from api.backend import *

if __name__ == '__main__':
    finism = Finism()
    stock_history = finism.stock_history()
    
    data = list(stock_history.items())
    for stock in data:
        (name, symbol), financials = stock
        
        subplots = [
            mpf.make_addplot(
                financials['macd'],
                ylabel = 'MACD',
                color = 'black',
                type = 'bar',
                panel = 1
            ),
            mpf.make_addplot(
                financials['rsi'],
                ylabel = 'RSI',
                color = 'black',
                panel = 2
            ),
            mpf.make_addplot(
                financials['sma'],
                color = 'blue',
                type = 'line'
            ),
            mpf.make_addplot(
                financials['ema'],
                color = 'yellow',
                type = 'line'
            )
        ]
        mpf.plot(
            financials,
            axtitle = f'{name}, ${symbol}',
            type = 'candle',
            style = 'yahoo',
            main_panel = 0,
            volume_panel = 3,
            addplot = subplots
        )
    mpf.show()