import toml
import pandas as pd
from src.cryptism import *
from src.cryptism import key
from src.stockism import *
from src.technical_analysis import *

FIAT = 'USD'

symbols = toml.load(
    'symbols.toml'
)

queue = {}
for classification, value in symbols.items():
    queue[classification] = {}
    for v in value:
        name, symbol = v.split(',')
        queue[classification].update({
            (name, symbol): {}
        })
symbols = queue

for ticker in symbols['stock'].keys():
    print(ticker)
    name, symbol = ticker
    stockism = Stockism(symbol)
    
    data = stockism.history(
        period.YEAR,
        interval.DAY
    )

    ta = TechnicalAnalysis(
        data,
        close = history.CLOSE,
        window = 20
    )

    ta.sma()
    ta.ema()
    ta.macd()
    ta.rsi()

    symbols['stock'][ticker] = data

for ticker in symbols['crypto'].keys():
    symbols['crypto'][ticker] = {
        key.PRICE: {}
    }

while True:
    for ticker in symbols['crypto'].keys():
        name, symbol = ticker
        print(ticker)
        cryptism = Cryptism()
        listing = cryptism.listing(
            symbol
        )
        
        local = cryptism.ticker(
            listing,
            convert = FIAT,
            keys = [
                key.RANK,
                key.CIRCULATING_SUPPLY,
                key.TOTAL_SUPPLY,
                key.PRICE,
                key.VOLUME_24H,
                key.MARKET_CAP,
                key.TIMESTAMP
            ]
        )

        symbols['crypto'][ticker][key.PRICE].update({
            pd.to_datetime(
                local[key.TIMESTAMP],
                unit = 's'
            ): local[key.PRICE]
        })
    
        
        ta = TechnicalAnalysis(
            symbols['crypto'][ticker],
            close = key.PRICE,
            window = 5
        )

        ta.sma()
        ta.ema()
        ta.macd()
        ta.rsi()