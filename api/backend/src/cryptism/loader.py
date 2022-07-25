from toml import load

ROOT_PATH = 'api/backend/src/cryptism'

def toml(local_path: str) -> dict:
    filepath = '/'.join((
        ROOT_PATH,
        local_path
    ))
    return load(filepath)