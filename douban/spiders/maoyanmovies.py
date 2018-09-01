# -*- coding: utf-8 -*-
import scrapy
import json
import re
import base64
from douban.items import ReYingMovie
from datetime import datetime
import requests
from douban.spiders.fonthelper import *




class MaoyanMoviesSpider(scrapy.Spider):

    name = "maoyanmovies"
    reyinurl = ["http://maoyan.com/films?showType=2&sortId=2&offset=%s"]
    fontMapping = []

    def start_requests(self):
        # self.server = connection.from_settings(self.settings)
        for template in self.reyinurl:
            for i in range(0,3):
                url = template %(i*20)
                yield scrapy.Request(url)

    def parse(self, response):
        urls = response.xpath('//div[@class="channel-detail movie-item-title"]/a/@href').extract()
        for i in urls:
            next_url = "http://maoyan.com"+i
            yield scrapy.Request(next_url, callback=self.parse_grade)


    def parse_grade(self,response):
        item =ReYingMovie()
        woff =response.xpath("//style/text()").extract_first()
        woffurl = 'http://'+re.findall(r'url\(\'//(.*?.woff)',woff)[0]
        woffdata = requests.get(woffurl).content
        b64 = base64.b64encode(woffdata)
        fontMapping = extract_fonts(b64)
        item["name"] = response.xpath('//h3[@class="name"]/text()').extract_first()
        item["createdtime"]=str(datetime.now())
        item["movieDate"]=response.xpath('//li[@class="ellipsis"][3]/text()').extract_first()[:-4]
        item["comefrom"]="猫眼"
        item["filmid"] = re.findall(r'\d+', response.url)[0]
        item["crawldate"] = str(datetime.today())
        people = response.xpath(
            '//div[@class="movie-index-content score normal-score"]/div/span/span/text()').extract_first()
        if people!=None:
            gradeor = response.xpath(
                '//div[@class="movie-index-content score normal-score"]/span/span/text()').extract_first()
            grade = self.decode_value(fontMapping, gradeor)
            item["Grade"] = grade
            people = response.xpath(
                '//div[@class="movie-index-content score normal-score"]/div/span/span/text()').extract_first()
            realpeo = self.decode_value(fontMapping, people)
            item["gradePeople"] = realpeo
            piaofang = response.xpath('//div[@class="movie-index"][2]/div/span/text()').extract_first()
            realpiao = self.decode_value(fontMapping, piaofang) + response.xpath('//div[@class="movie-index"][2]/div/span[2]/text()').extract_first()
            item['piaofang'] = realpiao
            return item

        else:
            item["name"] = response.xpath('//h3[@class="name"]/text()').extract_first()
            item["createdtime"] = str(datetime.now())

            item["movieDate"] = response.xpath('//li[@class="ellipsis"][3]/text()').extract_first()[:-4]
            want=response.xpath('//div[@class="movie-index-content score normal-score"]/span/span/text()').extract_first()
            wantpeople=self.decode_value(fontMapping,want)
            item["want"]=wantpeople
            item["comefrom"]="猫眼"
            print(item)
            return item

    def decode_value(self, fontMapping, rawdata):
        if rawdata == None:
            return None
        charts = []
        for chart in rawdata:
            decimalCode = ord(chart)
            if str(decimalCode) in fontMapping:
                charts.append(str(fontMapping[str(decimalCode)]))
            else:
                charts.append(chart)
        return ''.join(charts)
