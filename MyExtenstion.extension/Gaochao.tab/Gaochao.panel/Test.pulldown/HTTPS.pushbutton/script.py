# -*- coding: utf-8 -*-
__doc__ = "HTTPSREQUEST"

import urllib      #负责url编码处理
import urllib2
import json

class ApiPrice:
    def __init__(self,mcoder,coder):
        self.mcoder=mcoder
        self.coder=coder
        self.cost=''
    def BPrice(self):
        url = "http://101.200.166.88:90/api/Main/BPrice/"

        word = {"mcoder": self.mcoder, "coder": self.coder, "format": "json"}
        word = urllib.urlencode(word)

        # url首个分隔符就是 ?
        newurl = url + "?" + word
        headers = {'User-Agent': 'Mozilla 5.10', "Authorization": "Token cc32ff12efa240f6048069332b404d7eacc2e301",
                   "Content-Type": "application/json"}

        request = urllib2.Request(newurl, headers=headers)

        response = urllib2.urlopen(request)

        _data=response.read().decode('utf-8')

        _data=json.loads(_data)
        self.cost=_data[0].get('bprice')
        return _data[0]








coder=("15-03.10.12:5-47","15-03.10.12:5-46","15-03.10.12:5-45","15-03.10.12:5-44","15-03.10.12:5-43","15-03.10.12:5-42")
data=[]


for i in coder:
    _coder=i.split(":")
    mcoder=_coder[0]
    coder=_coder[1]
    _data=ApiPrice(mcoder,coder)
    print(_data)
    data.append(_data.BPrice())





from pyrevit import script

output = script.get_output()

result=[]
for i in data:
    a=[i.get('mcoder'),i.get('coder'),i.get('coder_name'),i.get('rengon_price'),i.get('cailiao_price'),i.get('jixie_price'),i.get('jixie_price')]
    result.append(a)


# formats contains formatting strings for each column
# last_line_style contains css styling code for the last line
output.print_table(table_data=result,
                   title="北京市建筑概算定额",
                   columns=["表15编码","详细编码","材料名称", "人工价格",  "材料价格","机械价格","概算价格"],
                   formats=['', '', '', '', '', '','',''],
                   last_line_style='color:red;')
