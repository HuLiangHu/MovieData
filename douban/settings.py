import os
# -*- coding: utf-8 -*-
# from .zz_proxies import get_ip
# Scrapy settings for tieba project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'douban'

SPIDER_MODULES = ['douban.spiders']
NEWSPIDER_MODULE = 'douban.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Maoyan (+http://www.yourdomain.com)'

MYSQL_HOST = os.environ['MYSQL_HOST'] if 'MYSQL_HOST' in os.environ else  ''
MYSQL_DBNAME = os.environ['MYSQL_DBNAME'] if 'MYSQL_DBNAME' in os.environ else 'newmedia_db'
MYSQL_USER = os.environ['MYSQL_USER'] if 'MYSQL_USER' in os.environ else ''
MYSQL_PASSWD = os.environ['MYSQL_PASSWD'] if 'MYSQL_PASSWD' in os.environ else ''
MYSQL_PORT = os.environ['MYSQL_PORT'] if 'MYSQL_PORT' in os.environ else  3306


MONGOD_URL = os.environ['MONGOD_URL'] if 'MONGOD_URL' in os.environ else  'mongodb://121.43.167.221:27017,120.27.227.216:27017/media?readPreference=secondaryPreferred'
# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'

'''
REDIS_URL = os.environ['REDIS_URL'] if 'REDIS_URL' in os.environ else 'redis://localhost:6379'
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_ORDER = 'BFO'
# Don't cleanup redis queues, allows to pause/resume crawls.
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
'''
DOWNLOAD_DELAY = 3
# Enables scheduling storing requests queue in redis.
#SCHEDULER = "scrapy_redis.scheduler.Scheduler"


SCHEDULER_PERSIST = True

RETRY_TIMES = 3

SCHEDULER_IDLE_BEFORE_CLOSE = 10

# Schedule requests using a priority queue. (default)
#SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'tieba (+http://www.yourdomain.com)'

LOG_LEVEL = 'ERROR'
#LOG_FILE = 'log.txt'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'douban.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'douban.middlewares.RandomProxy': 200,
#    'douban.middlewares.RandomUserAgent':300,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'douban.pipelines.MySqlPipeline': 300,
}

# '''
# SPLASH_URL = 'http://127.0.0.1:8050'
# #
# #MAIL_FROM:'webplay_MDS@data4media.com'
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_splash.SplashCookiesMiddleware': 723,
#     'scrapy_splash.SplashMiddleware': 725,
#     'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }
# '''
#
#STATS_CLASS = 'scrapy.statscollectors.MemoryStatsCollector'
#
# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
# IPLIST =get_ip.get_iplist()
