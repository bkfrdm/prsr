import csv
import collections
import threading
from time import sleep

import requests
import lxml.html, cssselect


from prsr import HDParser


class Engine:
    """ Persistent requests wrapper.
    Handles all errors except system ones,
    until counter reaches MAX_RETRY value.

    All methods:
    -> requests.Response
    """
    MAX_RETRY = 3
    DELAY = 1.5

    def GET(self, *args, **kwargs):
        errors = 0
        while True:
            try:
                sleep(self.DELAY)
                response = requests.post(*args, **kwargs)
                response.raise_for_status()
                return response
            
            except Exception as e:
                if errors == self.MAX_RETRY:
                    raise ConnectionError(e)
                
                print(e.__class__.__name__, e)
                errors += 1
    
    def POST(self, *args, **kwargs):
        errors = 0
        while True:
            try:
                sleep(self.DELAY)
                response = requests.post(*args, **kwargs)
                response.raise_for_status()
                return response
            
            except Exception as e:
                if errors == self.MAX_RETRY:
                    raise ConnectionError(e)
                
                print(e.__class__.__name__, e)
                errors += 1

class Scrpr(Engine):
    pass

def csv_out(filename, CSV_HEADERS, DATA, encoding='utf-8-sig'):
        with open(filename, 'w', encoding=encoding) as OUT:
            OUT = csv.writer(OUT, delimiter=';', lineterminator='\n', escapechar='\\')
            OUT.writerow(CSV_HEADERS)

            for row in DATA['rows']:
                OUT.writerow([row.get(h, '-') for h in CSV_HEADERS])
