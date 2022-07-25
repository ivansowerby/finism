import pandas as pd
from ta.volatility import *
from ta.volume import *
from ta.trend import *
from ta.momentum import *

class TechnicalAnalysis:
    def __init__(self, data: dict, close: str, window: int) -> None:
        self.df = pd.DataFrame.from_dict(
            data
        ).dropna()
        self.close = close
        self.window = window
    
    def sma(self, window: int = None):
        if window == None:
            window = self.window
        i = SMAIndicator(
            self.df[self.close],
            window
        )
        self.df['sma'] = i.sma_indicator()
    
    def ema(self, window: int = None):
        if window == None:
            window = self.window
        i = EMAIndicator(
            self.df[self.close],
            window
        )
        self.df['ema'] = i.ema_indicator()
    
    def macd(self):
        i = MACD(
            self.df[self.close],
        )
        self.df['macd'] = i.macd_signal()
    
    def rsi(self, window: int = None):
        if window == None:
            window = self.window
        i = RSIIndicator(
            self.df[self.close],
            window
        )
        self.df['rsi'] = i.rsi()
        
    def export(self):
        return self.df.to_json()