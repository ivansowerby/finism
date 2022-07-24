import toml
import pandas as pd
from src.cryptism import *
from src.cryptism import key
from src.stockism import *
from src.technical_analysis import *

class Finism:
    FIAT = 'USD'
    
    def __init__(self) -> None:
        self.symbols = toml.load(
            'symbols.toml'
        )

    def stock_history(self):
        queue = {}
        for classification, value in self.symbols.items():
            queue[classification] = {}
            for v in value:
                name, symbol = v.split(',')
                queue[classification].update({
                    (name, symbol): {}
                })
        self.symbols = queue

        for ticker in self.symbols['stock'].keys():
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

            data = ta.export()
            self.symbols['stock'][ticker] = data
            return data

    def crypto_live(self):
        for ticker in self.symbols['crypto'].keys():
            if key.PRICE not in ticker:
                self.symbols['crypto'][ticker]['price'] = {}

        for ticker in self.symbols['crypto'].keys():
            name, symbol = ticker
            print(ticker)
            cryptism = Cryptism()
            listing = cryptism.listing(
                symbol
            )
            
            local = cryptism.ticker(
                listing,
                convert = Finism.FIAT,
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

            self.symbols['crypto'][ticker][key.PRICE].update({
                pd.to_datetime(
                    local[key.TIMESTAMP],
                    unit = 's'
                ): local[key.PRICE]
            })
        
            
            ta = TechnicalAnalysis(
                self.symbols['crypto'][ticker],
                close = key.PRICE,
                window = 5
            )

            ta.sma()
            ta.ema()
            ta.macd()
            ta.rsi()

            return ta.export()