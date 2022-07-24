from toml import load

ROOT_PATH = 'src/stockism'

def toml(local_path: str) -> dict:
    filepath = '/'.join((
        ROOT_PATH,
        local_path
    ))
    return load(filepath)