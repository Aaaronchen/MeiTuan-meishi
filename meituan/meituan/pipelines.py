# -*- coding: utf-8 -*-

# Define your item pipelines here
# Author AaaronChen
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from meituan.items import MeiShi
from scrapy.exceptions import DropItem
from scrapy import Request
import pymysql,time
from scrapy.utils.project import get_project_settings

class MeituanPipeline(object):
    def __init__(self,host2,user2,password2,database2,port2):
        self.host2 = host2
        self.user2 = user2
        self.password2 = password2
        self.database2 = database2
        self.port2 = port2
 
    @classmethod
    def from_crawler(cls,crawler):
        '''注入实例化对象（传入参数）'''
        return cls(
            host2 = crawler.settings.get("MYSQL_HOST"),
            user2 = crawler.settings.get("MYSQL_USER"),
            password2 = crawler.settings.get("MYSQL_PASS"),
            database2 = crawler.settings.get("MYSQL_DATABASE"),
            port2 = crawler.settings.get("MYSQL_PORT"),
        )

    def open_spider(self, spider):
        '''负责连接数据库'''
        while not self.Connect():
            time.sleep(0.5)


    def process_item(self, item, spider):
        if isinstance(item, MeiShi):
            self.meishiItemprocess(item,spider)



    def close_spider(self, spider):
        '''关闭连接数据库'''
        self.db.close()


    def Connect(self):
        try:
            self.db = pymysql.connect(self.host2,self.user2,self.password2,self.database2,charset='utf8mb4',port=self.port2)
            if self.db:
                print("数据库连接成功")
                self.cursor = self.db.cursor()
                return self.db,self.cursor
        except Exception as e:
            print('数据库连接失败！！原因：',e)
        return None


    def pingConnect(self):
        try:
            self.db.ping()
        except:
            print('正在尝试数据库重连...')
            while not self.Connect():
                time.sleep(1)


    def meishiItemprocess(self, item, spider):
        '''执行数据表的写入操作'''
        data = {
            'avgPrice' : item['avgPrice'],
            'cateName' : item['cateName'],
            'channel' : item['channel'],
            'frontImg' : item['frontImg'],
            'lat' : item['lat'],
            'lng' : item['lng'],
            'name' : item['name'],
            'poiid' : item['poiid'],
            'areaName' : item['areaName'],
            'ctPoi' :item['ctPoi'],
            'adress' : item['adress'],
            'phone' : item['phone'],
            'openinfo' : item['openinfo'],
        }
        settings = get_project_settings()
        table = settings.get("MEISHITABLE")
        keys = ','.join(data.keys())
        values = ','.join(['%s'] * len(data))
        sql = "insert into {table} ({keys}) values ({values})".format(table=table,keys=keys,values=values)
        self.pingConnect()
        try:
            if self.cursor.execute(sql,tuple(data.values())):
                print("Successful........!")
                self.db.commit()

        except Exception as e:
            print('Failed:',e)
        return item
