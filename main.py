import prsr as Parser



with Parser('_gh', '_prx.txt') as get, Parser('_ph', '_pd', '_prx.txt') as post:
    url = 'http://xhaus.com/headers'
    Get.request(url)

    print(Get.response.text)


with Parser('_gh', '_prx.txt') as get, Parser('_ph', '_pd', '_prx.txt') as post:
    get(URL)
    
    tgt1 = get.select('body div div div h2 span')
    self.assertEqual(tgt1, ']')

    tgt2 = get.select('#Film')
    self.assertEqual(tgt2, 'Film')

