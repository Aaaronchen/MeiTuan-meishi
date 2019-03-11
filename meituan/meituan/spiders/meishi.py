# -*- coding: utf-8 -*-
# Author AaaronChen

import scrapy
import json,re
from scrapy.http import FormRequest
from meituan.items import MeiShi

class MeishiSpider(scrapy.Spider):
    name = 'meishi'
    allowed_domains = ['meituan.com']
    url = 'http://meishi.meituan.com/i/api/channel/deal/list'
    offset = 0
    areaList= [{"id":28,"name":"福田区","count":3878},{"id":29,"name":"罗湖区","count":1931},{"id":30,"name":"南山区","count":4038},{"id":32,"name":"宝安区","count":5344},{"id":33,"name":"龙岗区","count":4440},{"id":9553,"name":"龙华区","count":3344},{"id":31,"name":"盐田区","count":368},{"id":9535,"name":"南澳大鹏新区","count":79},{"id":23420,"name":"坪山区","count":345}]
    #areaList= [{"id":28,"name":"福田区","count":3878}]
    def start_requests(self):
        arealist = self.areaList
        for id in arealist:
            areaId = id['id']
            #areaname = id['name']
            yield self.before_request(str(areaId),str(self.offset))
            

    def before_request(self,areaId,offset):
        parms = {
            'app':"",
            'areaId':areaId,
            'cateId':'1',
            'deal_attr_23':"",
            'deal_attr_24':"",
            'deal_attr_25':"",
            'limit':'15',
            'lineId':'0',
            'offset':offset,
            'optimusCode':'10',
            'originUrl':"http://meishi.meituan.com/i/?ci=30&stid_b=1&cevent=imt%2Fhomepage%2Fcategory1%2F1",
            'partner':'126',
            'platform':'3',
            'poi_attr_20033':"",
            'poi_attr_20043':"",
            'riskLevel':'1',
            'sort':"default",
            'stationId':'0',
            'uuid':"ff5a7ab2968740cb84e7.1552011071.1.0.0",
            'version':"8.3.3",
        }
        return scrapy.FormRequest(url=self.url,method='POST',formdata=parms,callback=self.parse,dont_filter=True,meta={'areaId': areaId,'offset':offset,}) #FormRequest注意formdata的字典中不能用int,需要转换成str
        #方法二 
        #yield scrapy.Request(url=self.url, method='POST',body=json.dumps(parms), headers={'Content-Type':'application/json'} ) 


    def parse(self, response):
        res = response.body.decode("utf-8")
        #print(res)
        areaId = response.meta['areaId']
        offset = response.meta['offset']
        info = json.loads(res)
        if info:
            try:
                data = info.get('data')
                poiList = data.get('poiList')
                totalCount = poiList.get('totalCount')
                poiInfos = poiList.get('poiInfos')
                for i in poiInfos:
                    item = MeiShi()
                    item['avgPrice'] = i.get('avgPrice')
                    item['avgScore'] = i.get('avgScore')
                    item['cateName'] = i.get('cateName')
                    item['channel'] = i.get('channel')
                    item['frontImg'] = i.get('frontImg')
                    item['lat'] = i.get('lat')
                    item['lng'] = i.get('lng')
                    item['name'] = i.get('name')
                    item['poiid'] = i.get('poiid')
                    item['areaName'] = i.get('areaName')
                    item['ctPoi'] = i.get('ctPoi')
                    detail_url =  'https://meishi.meituan.com/i/poi/%s?ct_poi=%s'%(item['poiid'],item['ctPoi'])
                    print(detail_url)
                    yield scrapy.Request(url=detail_url,callback=self.parse_detail,dont_filter=True,meta={'item': item})
                print('地区%s已完成第%s页的爬取'%(areaId,str(int(offset)/15+1)))
                if int(totalCount) > int(offset):
                    offset = int(offset) + 15
                    yield self.before_request(areaId,str(offset))
                else:
                    print('地区%s已完成所有数据爬取...'%areaId)
            except Exception as e:
                print(e)

        else:
            print('Something Wrong! Get result:',res)


    def parse_detail(self,response):
        item = response.meta['item']
        html = response.body.decode("utf-8")
        phonepat = '"phone":"(.*?)"'
        addresspat = '"addr":"(.*?)"'
        openinfopat = '"openInfo":"(.*?)"'

        phonelist = re.findall(phonepat,html)
        addresslist = re.findall(addresspat,html)
        openinfolist = re.findall(openinfopat,html)
        item['adress'] = addresslist[0]
        item['phone'] = phonelist[0]
        openinfo = openinfolist[0].replace("\\n"," ")
        item['openinfo'] = openinfo
        print(item)
        yield item
        


