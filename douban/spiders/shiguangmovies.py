# -*- coding: utf-8 -*-
import scrapy
import json
import re
from douban.items import ReYingMovie
from datetime import datetime


# from scrapy_redis import connection


class ShiguangSpider(scrapy.Spider):

    name = "shiguangmovies"
    start_urls=['http://service.theater.mtime.com/Cinema.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Cinema.Services&Ajax_CallBackMethod=CinemaChannelIndexLoadData&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Ftheater.mtime.com%2FChina_Shanghai%2F&t=20188623115434461&Ajax_CallBackArgument0=253688%2C232758&Ajax_CallBackArgument1=&Ajax_CallBackArgument2=253688%2C255470%2C232758%2C256241%2C253904%2C257861%2C234573%2C233294%2C242167%2C247009%2C255796%2C256244%2C223748%2C225759%2C218440%2C223686%2C229451%2C229563%2C247608%2C228257%2C229631%2C259037%2C259271%2C250585%2C240989%2C240425%2C225725%2C255797%2C10053%2C225748%2C247241%2C229733%2C257482%2C241018%2C247420%2C228345%2C258591%2C230647%2C37575%2C259075%2C253951%2C129119%2C15523%2C225827%2C229275%2C257529%2C244236%2C233540%2C244987%2C233498%2C236921%2C229469%2C255265%2C222627%2C250925%2C254741%2C219285%2C247378%2C253011%2C250336%2C235583%2C250729%2C255302%2C217497%2C236671%2C253823%2C247295&Ajax_CallBackArgument3=258929%2C229275%2C225827%2C241018%2C257529%2C247506%2C142177%2C255265%2C258782%2C258531%2C258730%2C222627%2C258729%2C229469%2C250925%2C232096%2C255302%2C239726%2C257716%2C258677%2C257971%2C257733%2C257792%2C235042%2C258933%2C249775%2C259334%2C255708%2C259172%2C244991%2C228903%2C257780%2C235512%2C226992%2C257775%2C258573%2C250829%2C257487%2C255797%2C259292%2C242270%2C228277%2C258535%2C250339%2C218614%2C251499%2C254621%2C258469%2C250964%2C250539%2C225752%2C232552%2C254620%2C237903%2C242119%2C236593%2C236488%2C254645%2C253914%2C247505%2C235221']
    detail_url='http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackMethod=GetMovieOverviewRating&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Fmovie.mtime.com%2F253688%2F&t=20188623322769205&Ajax_CallBackArgument0={}'
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    # def hotplay_requests(self):
    #     url='http://service.theater.mtime.com/Cinema.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Cinema.Services&Ajax_CallBackMethod=GetOnlineMoviesInCity&Ajax_CrossDomain=1&Ajax_RequestUrl=http%3A%2F%2Ftheater.mtime.com%2FChina_Shanghai%2F&Ajax_CallBackArgument0=292'
    #     yield scrapy.Request(url,callback=self.parse_grade)
    # # def hotplay_parse(self,response):
    def parse(self, response):
        jsonstr=re.findall('var result_\d+ = (.*);var',response.text)[0]
        item = ReYingMovie()
        for i in json.loads(jsonstr)['value']['hotplayRatingList']:
            item["filmid"]=i['Id']
            url = self.detail_url.format(str(item['filmid']))
            # print(url)
            yield scrapy.Request(url, callback=self.parse_grade)

        for i in json.loads(jsonstr)['value']['upcomingTicketList']:
            item["filmid"] = i['Id']

            url=self.detail_url.format(str(item['filmid']))
            # print(url)
            yield scrapy.Request(url,callback=self.parse_grade)
    # def parse(self, response):
    #     jsonStr = re.search('var hotplaySvList = (\[.*\]);',response.text).group(1)
    #     items = json.loads(jsonStr)
    #
    #     for item in items:
    #         next_url=self.detail_url.format(item['Id'])
    #         yield scrapy.Request(next_url,callback=self.parse_grade)
    #     for url in response.xpath('//dl[@id="upcomingSlide"]/dd/ul/li/a/@href').extract():
    #         id= re.search('movie.mtime.com/(\d+)/',url).group(1)
    #         next_url=self.detail_url.format(id)
    #         yield scrapy.Request(next_url,callback=self.parse_grade)
    #

    def parse_grade(self,response):
        data = json.loads(re.findall(r'({.*})',response.text)[0])
        #print(data)
        #print(data['value']['movieRating']['RatingFinal'])
        item = ReYingMovie()
        item["createdtime"]=str(datetime.now())
        item["comefrom"]="时光"
        item['name']=data['value']['movieTitle']
        item["Grade"] =data['value']['movieRating']["RatingFinal"]
        if item["Grade"]<0:
            item["Grade"]=None
        item["gradePeople"] = data['value']['movieRating']["Usercount"]
        item["want"] = data['value']['movieRating']["AttitudeCount"]
        item["music"] = data['value']['movieRating']["ROtherFinal"]
        item["frames"] = data['value']['movieRating']["RPictureFinal"]
        item["story"] = data['value']['movieRating']["RStoryFinal"]
        item["director"] = data['value']['movieRating']["RDirectorFinal"]
        item["filmid"]=data['value']['movieRating']['MovieId']
        item["crawldate"]=str(datetime.today())
        #print(item)
        return item

