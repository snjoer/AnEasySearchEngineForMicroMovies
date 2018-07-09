# -*- encoding:utf-8 -*-

import re
import sys
import scrapy 
from bs4 import BeautifulSoup
from VMovie.items import XinItem
from scrapy_redis.spiders import RedisSpider

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieLinkSpider(RedisSpider):
    name = 'xin'
    redis_key = 'xinurl'

    def parse(self, response):
        item = XinItem2()
	title = response.xpath('//div[@class="vsns-main"]//h1/text()').extract_first()
        content = ''.join(''.join(response.xpath('//div[@class="film_intro"]//text()').extract()).split())
        channel = response.xpath('//div[@class="clearfix film_intro"]/a/text()').extract_first()
        
        item['content'] = content
        item['channel'] = channel

#        hv = hash(title)            
#        with open(str(hv) + '.html', 'w') as f:
#            f.write(response.text)  

        yield item
