import requests
import json

class Fetcher(object):
    """docstring for Fetcher."""
    def __init__(self, url):
        super(Fetcher, self).__init__()
        self.url = url
        self.data = []

    def call(self):
        data = requests.get(self.url)
        self.data = json.loads(data.text)

        return self.data
