# -*- encoding:utf-8 -*-

import re
import sys
import scrapy 
import redis
import hashlib
from bs4 import BeautifulSoup
from VMovie.items import XinItem

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieLinkSpider(scrapy.Spider):
    page = 1
    pre_url = 'http://www.xinpianchang.com/channel/index/type-0/sort-like/page-'
    name = 'XinLink'
    r = redis.Redis(host='localhost', port=6379)

    def start_requests(self):
        url = self.pre_url + str(self.page)
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        lists = response.xpath('//ul[@class="film-list clearfix"]/li')
        for li in lists:
            item = XinItem()
            title = li.xpath('a/img/@title').extract_first()
            link = li.xpath('a/@href').extract_first()
            poster = li.xpath('a/img/@src').extract_first()
            time = li.xpath('.//span[@class="master-type-date"]/text()').extract_first()
            time = re.findall(r'[0-9]*-[0-9]*-[0-9]*', time)[0]
            author = li.xpath('.//span[@class="overdot inb"]/text()').extract_first()
            data = li.xpath('.//span[@class="film-footer-num overdot"]//text()').extract()
            duration = li.xpath('.//span[@class="tm"]/text()').extract_first()
            play = ''.join(data[1].split())
            like = ''.join(data[3].split())
            comment = ''.join(data[5].split())
            encrypts = hashlib.sha1(poster).hexdigest()
            item['title'] = title
            item['link'] = link
            item['image_urls'] = [poster]
            item['poster'] = encrypts
            item['time'] = time
            item['author'] = author
            item['like'] = like
            item['comment'] = comment
            item['play'] = play
            item['rating'] = None
            item['duration'] = duration
#            self.r.lpush('xinurl', link)
            yield scrapy.Request(link, callback=self.parse_detail, meta={'item':item})
        self.page += 1
        if self.page == 3586:
            return
        url = self.pre_url + str(self.page)
        yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        title = response.xpath('//div[@class="vsns-main"]//h1/text()').extract_first()
        content = ''.join(''.join(response.xpath('//div[@class="film_intro"]//text()').extract()).split())
        channel = response.xpath('//div[@class="clearfix film_intro"]/a/text()').extract_first()
            
        item['content'] = content
        item['channel'] = channel
   
        yield item
