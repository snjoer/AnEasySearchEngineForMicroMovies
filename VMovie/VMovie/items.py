# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VmovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    link = scrapy.Field()
    title = scrapy.Field()
    image_urls = scrapy.Field()
    poster = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    author = scrapy.Field()
    time = scrapy.Field()
    content = scrapy.Field()
    channel = scrapy.Field()
    play = scrapy.Field()

class XinItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    image_urls = scrapy.Field()
    poster = scrapy.Field()
    time = scrapy.Field()   
    author = scrapy.Field()
    like = scrapy.Field()
    comment = scrapy.Field()
    play = scrapy.Field()   
    rating = scrapy.Field()
    duration = scrapy.Field()
    content = scrapy.Field()
    channel = scrapy.Field()
