# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class UnivItem(scrapy.Item):
	name = scrapy.Field()
	country = scrapy.Field()
	state = scrapy.Field() #only US
	city = scrapy.Field()
	website = scrapy.Field()
