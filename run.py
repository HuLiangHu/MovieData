import scrapy
from scrapy.crawler import CrawlerProcess
from douban.spiders.doubanmovies import DoubanMoviesSpider
from douban.spiders.maoyanmoviesnew import MaoyanNewSpider

from douban.spiders.taopiaopiaomovies import TaoMoviesSpider





from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())
# process.crawl(DoubanMoviesSpider)
# #process.crawl(GewalaMoviesSpider)
# process.crawl(MaoyanNewSpider)
# #process.crawl(NuomiMoviesSpider)
# process.crawl(ShiguangSpider)
process.crawl(TaoMoviesSpider)
#process.crawl(XinlangMoviesSpider)

#process.crawl(AudiencesSpider)
process.start() # the script will block here until all crawling jobs are finished