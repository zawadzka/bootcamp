# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MigrationItem(scrapy.Item):
    link_title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()

class DrugiItem(scrapy.Item):
    #link_title = scrapy.Field()
    url = scrapy.Field()
    text = scrapy.Field()
    h1 = scrapy.Field()
