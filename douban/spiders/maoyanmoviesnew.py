# -*- coding: utf-8 -*-
from datetime import datetime

import scrapy
import re
from scrapy.http import Request
from traceback import format_exc
from scrapy import Selector

from douban.spiders.Utils_model.font import font_creator
from ..items import  ReYingMovie


class MaoyanNewSpider(scrapy.Spider):
    name = 'maoyannew'
    allowed_domains =['book.qidian.com']
    start_urls =['https://book.qiandian.com']
    def start_requests(self):
        for url in self.start_urls:
             yield scrapy.Request(url, callback=self.pare_movielist)

    allowed_domains = ['maoyan.com', 'api.xdaili.cn', 'xdaili-api']

    start_urls = ['http://maoyan.com/films?showType=1',#正在热映
                  'http://maoyan.com/films?showType=2']#即将上映

    def start_requests(self):
        for url in self.start_urls:
             yield scrapy.Request(url, callback=self.pare_movielist)

    def pare_movielist(self,response):
        movie_links = response.xpath('//div[@class="movie-item"]/a/@href').extract()
        for link in movie_links:
            url='http://maoyan.com'+link
            #print(url)
            yield scrapy.Request(url,callback=self.parse_detail)
            next_url = response.xpath("//li/a[text()='下一页']/@href").extract_first()

            if next_url is not None:
                next_url = 'http://maoyan.com/films' + str(next_url)
                #print("下一页的链接:", next_url)
                yield Request(next_url,callback=self.pare_movielist)


    def parse_detail(self, response):

        html_font = font_creator(response.text)
        resp = Selector(text=html_font)
        item = ReYingMovie()

        container = "".join(resp.xpath('//div[@class="movie-stats-container"]//text()').extract()).split()

        item['name'] = response.xpath('//div[@class="movie-brief-container"]/h3/text()').extract_first()
        item["createdtime"] = str(datetime.now())
        item["movieDate"] = response.xpath('//li[@class="ellipsis"][3]/text()').extract_first()[:-4]
        item["comefrom"] = "猫眼"
        item["filmid"] = re.findall(r'\d+', response.url)[0]
        item["crawldate"] = str(datetime.today())
        item["createdtime"] = str(datetime.now())

        try:
            item['Grade'] = container[1]
            item['gradePeople'] = container[2]
            if '万' in item['gradePeople']:
                item['gradePeople']=float(re.findall('(\d+)',item['gradePeople'])[0])*10000
            elif '亿' in item['gradePeople']:
                item['gradePeople']=float(re.findall('(\d+)',item['gradePeople'])[0])*100000000
            else:
                item['gradePeople']=int(re.findall('(\d+)',item['gradePeople'])[0])
            item['piaofang'] = container[4]
            item['want'] = "None"
        except:
            item['Grade'] = "None"
            item['gradePeople'] = "None"
            item['piaofang'] = "None"
            item['want'] = container[1]
        print(item)
        yield item

    def error_back(self, e):
        """
        报错机制
        """
        self.logger.error(format_exc())
