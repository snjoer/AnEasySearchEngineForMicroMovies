# -*- encoding:utf-8 -*-
import json
import sys
import redis
import scrapy 
import hashlib
from bs4 import BeautifulSoup
from VMovie.items import VmovieItem

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieLinkSpider(scrapy.Spider):
    page = 1
    pre_url = 'http://www.vmovier.com/cate/getbycate?cate=1&tab=new&page='
    name = 'link'
    r = redis.Redis(host='localhost', port=6379)

    def start_requests(self):
        urls = []
        for i in xrange(0, 3):
            urls.append(self.pre_url + str(self.page) + '&pagepart=' + str(i))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        urls = []
        r = json.loads(response.body_as_unicode())
        status = r['status']
        if int(status) == -1:
            return
        data = r['data']
        soup = BeautifulSoup(data, 'lxml')
        lists = soup.find_all('li')
        for li in lists:
            item = VmovieItem()
            title = li.find('a')['title']
            poster = li.find('img')['src']
            like = li.find('span', title='喜欢数').text
            comment = li.find('span', title='评论数').text
            try:
                duration = li.find('span', {'class':'film-time'}).text
            except:
                duration = None
            try:
                rating = li.find('div', class_='rating')['data-score']
            except:
                rating = None
            link = response.urljoin(li.find('a')['href'])
            encrypts = hashlib.sha1(poster).hexdigest()
            item['title'] = title
            item['image_urls'] = [poster]
            item['poster'] = encrypts
            item['like'] = like
            item['comment'] = comment
            item['duration'] = duration
            item['rating'] = rating
            item['link'] = link
            yield scrapy.Request(link, callback=self.parse_detail, meta={'item':item})
        self.page += 1
        for i in xrange(0, 3):
            urls.append(self.pre_url + str(self.page) + '&pagepart=' + str(i))
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta['item']
        title = ''.join(response.xpath('//h1[@class="post-title"]/text()').extract_first().split())
        time = response.xpath('//span[@class="time"]/text()').extract_first()
        author = response.xpath('//span[@class="author"]/text()').extract_first() 
        try:
            content = ''.join(response.xpath('//span[@class="intro-wrap show-part"]//text()').extract())
            channel = response.xpath('//div[@class="channel"]/a/text()').extract_first()
        except:
            content = ''.join(response.xpath('//div[@class="post-main clearfix"]//p//text()').extract())
            channel = response.xpath('//span[@class="badge badge-green"]/text()').extract_first() 
        item['time'] = time
        item['content'] = content
        item['author'] = author
        item['channel'] = channel
        item['play'] = None
        
        yield item  
