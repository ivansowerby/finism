from sys import path
path.append(
    'api'
)

import backend.src.cryptism.loader as loader
import backend.src.cryptism.finder as finder
from backend.src.cryptism.api import *
from backend.src.cryptism.call import *

class Cryptism:
    def __init__(self) -> None:
        self.listings = fetch(
            urlify('listings')
        )
        self.build = loader.toml(
            'build.toml'
        )
        path = self.build['path']
        dependencies = self.build['dependencies']
        for file in dependencies.items():
            exec(
                f'self._{file[0]} = loader.toml("{file[1]}")'
            )

        self.history = []
    
    def listing(self, identity: str) -> dict:
        for currency in self.listings['data']:
            if any([True for i in currency.values() if i == identity]):
                return currency
    
    def __filter__(self, call: Call, keys: list, syntax: dict, filter: dict = None) -> dict:
        paths = []
        for type in syntax.items():
            path, variables = type
            for v in variables:
                for k in keys:
                    if v == k:
                        paths.append(
                            (path + '/' + k).split('/')
                        )
        
        data = {}
        for path in paths:
            data.update({
                path[-1]: finder.path(
                    call.data,
                    path,
                    filter
                )
            })
        return data

    def ticker(self, listing: dict, convert: str = "USD", structure: str = "dictionary", keys: list = None) -> dict:
        endpoint = self._endpoint['ticker']

        convert = convert.upper()
        fiat = endpoint['convert']['fiat']
        crypto = endpoint['convert']['crypto']
        if convert not in fiat:
            raise ValueError(
                f'{convert.upper()} is not a valid conversion currency,\n{fiat + crypto}'
            )
        
        structure = structure.lower()
        _structure = endpoint['structure']
        if structure not in _structure:
            raise ValueError(
                f'{structure} is not a valid structure,\n{_structure}'
            )
        
        url = query(
            endpoint = [
                'ticker',
                listing['website_slug']
            ],
            query = {
                'convert': convert,
                'structure': structure
            }
        )

        for call in self.history:
            if url == call.url and Call.interval(call):
                return call.data

        ticker = fetch(
            url
        )

        call = Call(
            url,
            ticker
        )

        self.history.append(
            call
        )

        if keys == None:
            return call.data
        
        data = self.__filter__(
            call,
            keys,
            syntax = self._ticker,
            filter = {
                'id': listing['id'],
                'convert': convert,
                'structure': structure
            }
        )

        return data
    
    def ranked_ticker(self, limit: int, convert: str = 'USD', structure: str = "dictionary"):
        endpoint = self._endpoint['ticker']

        limit = str(limit)
        if not limit.isdigit():
            raise ValueError(
                f'{limit} is not an interger digit'
            )

        structure = structure.lower()
        _structure = endpoint['structure']
        if structure not in _structure:
            raise ValueError(
                f'{structure} is not a valid structure,\n{_structure}'
            )
        
        request = {
            'limit': limit,
            'convert': convert,
            'structure': structure
        }

        url = query(
            endpoint = [
                'ticker',
            ],
            query = request
        )

        for call in self.history:
            if url == call.url and Call.interval(call):
                return call.data

        tickers = fetch(
            url
        )

        call = Call(
            url,
            tickers
        )

        self.history.append(
            call
        )

        return tickers

    def fear_and_greed(self, limit: int = 1, format: str = 'json', date_format = 'world', keys: list = None) -> dict:
        endpoint = self._endpoint['fng']
        
        limit = str(limit)
        if not limit.isdigit():
            raise ValueError(
                f'{limit} is not an interger digit'
            )

        _format = endpoint['format']
        if format not in _format:
            raise ValueError(
                f'{format} is not a valid format,\n{_format}'
            )
        
        _date_format = endpoint['date_format']
        if date_format not in _date_format:
            raise ValueError(
                f'{date_format} is not a valid date format,\n{_date_format}'
            )
        
        url = query(
            endpoint = [
                'fng',
            ],
            query = {
                'limit': limit,
                'format': format,
                'date_format': date_format
            }
        )

        for call in self.history:
            if url == call.url and Call.interval(call):
                return call.data

        fng = fetch(
            url
        )

        call = Call(
            url,
            fng
        )

        self.history.append(
            call
        )

        data = self.__filter__(
            call,
            keys,
            syntax = self._fng
        )

        return data


    def fng(self, limit: int = 1, format: str = 'json', date_format = 'world', keys: list = None) -> dict:
        return self.fear_and_greed(
            limit,
            format,
            date_format,
            keys
        )