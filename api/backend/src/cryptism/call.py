from time import time

class Call:
    INTERVAL = 5 * 60
    def __init__(self, url: str, data) -> None:
        self.url, self.data = url, data
        self.timestamp = time()
    
    def interval(call) -> bool:
        if time() + Call.INTERVAL > call.timestamp:
            return True
        else:
            return False