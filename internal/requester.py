from requests import get

class Requester:
    def __init__(self):
        self.url = "https://github.com/AURAK-Coding-Club"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    
    def get(self):
        return get(self.url, headers = self.headers)
    