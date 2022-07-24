from math import inf
import backend.src.stockism.period as period
import backend.src.stockism.interval as interval
import backend.src.stockism.history as history
import yfinance as yf
import pandas as pd
import datetime as dt
from backend.src.stockism.date import *

class Stockism:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.stock = yf.Ticker(
            symbol
        )
    
    def history(self, period: str = period.MAX, interval: str = interval.WEEK, keys: list = None) -> dict:
        data = pd.DataFrame.to_dict(self.stock.history(
            period,
            interval
        ))
        if keys == None:
            return data
        return {key: data[key] for key in keys}
    
    def filter_for(self, data: dict, keys: list) -> dict:
        return {key: data[key] for key in keys}
    
    def __equidistant__(n: int, packet: dict, cell: dict) -> dict:
        local = {}
        index = list(packet.keys()).index(
            *list(cell.keys()
        ))
        index = abs(index - n)
        
        l = list(packet.items())
        for i in range(index, 2 * n + index):
            k, v = l[i]
            local.update({
                k: v
            })
        return local

    def nth_nearby(data: dict, date: str, n: int, keys: list = None) -> dict:
        if keys == None:
            keys = data.keys()
        
        timestamp = unix_epoche(pd.Timestamp(
            date
        ))

        nearby = {}
        for key in keys:
            packet = data[key]
            closest, cell = inf, {}
            for k, v in packet.items():
                d = timestamp - unix_epoche(k)
                if abs(d) < closest:
                    closest = d
                    cell = {
                        k: v
                    }
            
            local = Stock.__equidistant__(
                n,
                packet,
                cell,
            )

            nearby.update({
                key: local
            })
        return nearby

    def day_equidistant(data: dict, date: str, days: int, keys: list = None) -> dict:
        if keys == None:
            keys = data.keys()
        
        timestamp = pd.Timestamp(
            date
        ) - dt.timedelta(days)
                
        ranges = {}
        for key in keys:
            packet = data[key]
            cell = {}
            for k, v in packet.items():
                date = k.date()
                if date >= timestamp and \
                   date < timestamp + dt.timedelta(days):
                    cell.update({
                        k: v
                    })
            
            local = Stock.__equidistant__(
                days,
                packet,
                cell,
            )

            ranges.update({
                key: local
            })
        return ranges