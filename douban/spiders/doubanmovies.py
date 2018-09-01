# -*- coding: utf-8 -*-
import scrapy
import json
import re
from scrapy.selector import Selector
import random
from datetime import datetime
from scrapy.utils.project import get_project_settings
import pymysql
from scrapy.http import HtmlResponse
import random
from douban.items import ReYingMovie
from datetime import datetime


# from scrapy_redis import connection

class DoubanMoviesSpider(scrapy.Spider):

    name = "doubanmovies"
    start_urls = ['https://movie.douban.com/cinema/nowplaying/shanghai/','https://movie.douban.com/coming']

    def parse(self, response):
        if re.match('^(http|https|ftp)\:\/\/movie.douban.com\/coming',response.url):
            detail_urls = response.xpath('//div[@class="grid-16-8 clearfix"]/div/table/tbody/tr/td/a[@href]/@href').extract()
            for url in detail_urls:
                yield scrapy.Request(url,callback=self.parse_grade)
        else:
            detail_urls = response.xpath('//*[@id="nowplaying"]/div[2]/ul/li/ul/li[@class="stitle"]/a[@href]/@href').extract()
            for url in detail_urls:
                yield scrapy.Request(url,callback=self.parse_grade)


    def parse_grade(self,response):
        selector = Selector(response)
        item = ReYingMovie()
        item["name"]=selector.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        item["createdtime"]=str(datetime.now())
        item["comefrom"]="豆瓣"
        item["filmid"]=selector.xpath('//span[@class="rec"]/a/@share-id').extract_first()
        item["crawldate"]=str(datetime.today())
        try:
            item["movieDate"]=selector.xpath('//span[@property="v:initialReleaseDate"]/text()').extract_first()
            item["Grade"] = selector.xpath('//strong[@property]/text()').extract_first()
            item["gradePeople"] = selector.xpath('//span[@property="v:votes"]/text()').extract_first()
            rating = selector.xpath('//span[@class="rating_per"]/text()').extract()
            if len(rating)>0:
                item["five"] = rating[0]
                item["four"] = rating[1]
                item["three"] = rating[2]
                item["two"] = rating[3]
                item["one"] = rating[4]
            item["want"]=selector.xpath('//div[@class="subject-others-interests-ft"]/a[2]/text()').extract_first()[:-3]
        except IndexError:
            item["movieDate"]=selector.xpath('//span[@property="v:initialReleaseDate"]/text()').extract_first()
            # item["Grade"] = ""
            # item["gradePeople"] = ""
            # item["five"] = ""
            # item["four"] = ""
            # item["three"] = ""
            # item["two"] = ""
            # item["one"] = ""
            item["want"]=selector.xpath('//div[@class="subject-others-interests-ft"]/a[2]/text()').extract_first()[:-3]
        return item

