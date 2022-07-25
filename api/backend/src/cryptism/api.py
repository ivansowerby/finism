from sys import path
path.append(
    'api'
)

import backend.src.cryptism.loader as loader
from requests import get

def fetch(url: str) -> dict:
    response = get(url)
    if response.status_code == 200:
        return response.json()

def urlify(endpoint: str) -> str:
    api = loader.toml(
        'api/api.toml'
    )
    if endpoint != 'fng':
        endpoint = 'v' + api['version'] + '/' + endpoint
    return '/'.join((
        api['base_url'],
        endpoint
    ))

def query(endpoint: list, query: dict) -> str:
    return urlify('/'.join(endpoint)) + '/?' + '&'.join(
        ['='.join(q) for q in query.items()]
    )