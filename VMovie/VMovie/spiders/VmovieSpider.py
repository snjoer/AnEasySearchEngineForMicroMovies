# -*- encoding:utf-8 -*-
import json
import sys
import scrapy 
from bs4 import BeautifulSoup
from VMovie.items import VmovieItem
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieSpider(RedisSpider):
    name = 'movie'
    redis_key = 'url'

    def parse(self, response):
        item = VmovieItem2()
        title = ''.join(response.xpath('//h1[@class="post-title"]/text()').extract_first().split())
        time = response.xpath('//span[@class="time"]/text()').extract_first()
        author = response.xpath('//span[@class="author"]/text()').extract_first() 
        try:
            content = ''.join(response.xpath('//span[@class="intro-wrap show-part"]//text()').extract())
            channel = response.xpath('//div[@class="channel"]/a/text()').extract_first()
        except:
            content = ''.join(response.xpath('//div[@class="post-main clearfix"]//p//text()').extract())
            channel = response.xpath('//span[@class="badge badge-green"]/text()').extract_first() 
        item['link'] = response.url
        item['time'] = time
        item['content'] = content
        item['author'] = author
        item['channel'] = channel
        item['play'] = None
    
        hv = hash(title)
        with open(str(hv) + '.html', 'w') as f:
            f.write(response.text)

        yield item
