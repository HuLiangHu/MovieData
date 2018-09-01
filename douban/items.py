# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ReYingMovie(scrapy.Item):
    name = scrapy.Field(default=0)
    createdtime=scrapy.Field(default=0)
    comefrom=scrapy.Field(default=0)
    movieDate = scrapy.Field(default=0)
    Grade = scrapy.Field(default=0)
    gradePeople = scrapy.Field(default=0)
    five = scrapy.Field(default=0)
    four = scrapy.Field(default=0)
    three = scrapy.Field(default=0)
    two = scrapy.Field(default=0)
    one = scrapy.Field(default=0)
    want = scrapy.Field(default=0)
    good = scrapy.Field(default=0)
    bad = scrapy.Field(default=0)
    music = scrapy.Field(default=0)
    story = scrapy.Field(default=0)
    director = scrapy.Field(default=0)
    frames = scrapy.Field(default=0)
    piaofang=scrapy.Field(default=0)
    crawldate=scrapy.Field()
    filmid=scrapy.Field()




    