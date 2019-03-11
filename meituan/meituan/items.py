# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# Author AaaronChen
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class MeiShi(scrapy.Item):
    avgPrice = scrapy.Field()
    avgScore = scrapy.Field()
    cateName = scrapy.Field()
    channel = scrapy.Field()
    frontImg = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    name = scrapy.Field()
    poiid = scrapy.Field()
    areaName = scrapy.Field()
    ctPoi = scrapy.Field()
    adress = scrapy.Field()
    phone = scrapy.Field()
    openinfo = scrapy.Field()
