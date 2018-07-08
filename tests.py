import unittest

from prsr import Parser




URL = 'https://httpbin.org'


class PrsrTest(unittest.TestCase):

    def test_Parser_returns_Parser_instance_object(self):
        get = Parser()
        self.assertIsInstance(get, Parser)

    def test_Parser_gets_correct_headers(self):
        get = Parser('_gh.txt')
        with open('_gh.txt') as file:
            header, *header_values = file.readline().split(':')

        self.assertEqual(get.headers[header], ':'.join(header_values).strip())

    def test_Parser_context_managers_supported(self):
        with Parser('_gh.txt') as get:
            self.assertIsInstance(get, Parser)

    def test_Parser_instance_call_makes_GET_request(self):
        with Parser('_gh.txt') as get:
            get(URL + '/get')
            self.assertEqual(get.status, 200)

           

    

        



        
    """
    with Parser('_gh', '_prx.txt') as get, Parser('_ph', '_pd', '_prx.txt') as post:
        get(URL)
        
        tgt1 = get.select('body div div div h2 span')
        self.assertEqual(tgt1, ']')

        tgt2 = get.select('#Film')
        self.assertEqual(tgt2, 'Film')
    """





if __name__ == '__main__':
    unittest.main(verbosity=2)
