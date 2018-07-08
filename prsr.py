import time
from abc import abstractmethod, ABCMeta

import requests

from hprsr import HDParser




class ParserErrors(Exception):
    pass


class ParserResponseInvalidStatusCode(ParserErrors):
    pass


class ParserMaxRetiresReached(ParserErrors):
    pass


class ProperEngine(metaclass=ABCMeta):
    @abstractmethod
    def get(url):
        pass

    @abstractmethod
    def post(url):
        pass

    @staticmethod
    def persistent_request(meth):
        def wrapper(url, *, timeout=0.5, max_retries=1, codes_valid=[200,], **kwargs):
            retries = 0
            kwargs = {k: v for k, v in kwargs.items() if k in ['headers', 'data', 'proxies']}
            while retries < max_retries:
                try:
                    print(*[(k.rjust(20), repr(v)[:20]) for k, v in kwargs.items()], sep='\n')
                    response = meth(url, **kwargs)
                    print('In deco', response)

                    if response.status_code in codes_valid: return response
                    else: raise ParserResponseInvalidStatusCode(f'{response} not in {codes_valid}')
                    
                except ParserErrors as exc:
                    exc_last = exc
                    retries += 1
                    print(f'ProperEngine.persistent_request {retries}/{max_retries}\n\t {exc.__class__.__name__}: {exc}')
                    time.sleep(timeout)
            raise ParserMaxRetiresExceeded(f'{exc_last.__class__.__name__}: {exc_last}')
        return wrapper
        
    

class Parser(metaclass=ABCMeta):
    def __init__(self, headers=None, data=None, proxies=None):
        self.proxies = proxies
        self.headers = HDParser(headers)
        self.data = HDParser(data)
        
        if data: self.method = 'POST'
        else: self.method = 'GET'

        self.engines = {cls.__name__.lower(): cls for cls in Parser.__subclasses__()}
        self.response = None

    def __enter__(self, *args, **kwargs):
        return Parser(*args, **kwargs)

    def __exit__(self, exc_cls, exc_inst, exc_trace):
        pass

    def __call__(self, url, *, engine='requests', **kwargs):
        engine = self.engines[engine]
        if self.method == 'GET':
            self.response = engine.get(url, headers=self.headers, proxies=self.proxies, **kwargs)
        elif self.method == 'POST':
            self.response = engine.post(url, headers=self.headers, data=self.data, proxies=self.proxies, **kwargs)

    @property
    def status(self):
        if self.response:
            return self.response.status_code
        

class Requests(Parser, ProperEngine):

    @ProperEngine.persistent_request
    def get(url, **kwargs):
        return requests.get(url, **kwargs)

    @ProperEngine.persistent_request
    def post(url, **kwargs):
        return requests.post(url, **kwargs)




if __name__ == '__main__':
    get = Parser('_gh.txt')
    post = Parser('_gh.txt', data={'test_name': 'test_value'})
    [o.headers.pops('Host') for o in (get, post)]
    
    print('\n\n\n--------- GET       ---------')
    get('https://httpbin.org' + '/get')
    print(get.response)
    print(get.response.json())

    print('\n\n\n--------- POST      ---------')
    post('https://httpbin.org' + '/post')
    print(post.response)
    print(post.response.json())

    print('\n\n\n--------- GET FAILS       ---------')
    try:
        get('https://httpbin.org' + '/gets', max_retries=5, timeout=1)
    except Exception:
        print('Handled')

    print('\n\n\n--------- POST FAILS      ---------')
    post('https://httpbin.org' + '/posts', max_retries=5, timeout=1)
    
