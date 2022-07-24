from datetime import timedelta
import pandas as pd
import src.stockism.loader as loader

def date(year: int, month: int= 1, day: int = 1, \
         hour: int = 0, minute: int = 0, second: int = 0) -> str:
    ymd = []
    set = (year, month, day, hour, minute, second)
    length = (4, 2, 2, 2, 2, 2)
    for t, l in zip(set, length):
        t = str(t)
        if len(t) < l:
            t = t.zfill(l)
        ymd.append(t)
            
    return '-'.join(ymd[0:2]) + ' ' + ':'.join(ymd[3:len(ymd)])

def unix_epoche(timestamp: pd.Timestamp) -> int:
    return (
        timestamp - pd.Timestamp(
            '1960-01-01'
        )
    ) // pd.Timedelta('1s')

def frame(n: float, unit: str = 'day') -> str:
    units = loader.toml(
        'frame.toml'
    )['units']
    
    for k, v in units.items():
        v.insert(0, k)
        if unit.lower() in v:
            if n != 1:
                unit = v[0]
            else:
                unit = v[-1]     
    return ' '.join((
        str(n), unit
    ))