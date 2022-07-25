from toml import load

ROOT_PATH = 'api/backend/src/stockism'

def toml(local_path: str) -> dict:
    filepath = '/'.join((
        ROOT_PATH,
        local_path
    ))
    return load(filepath)