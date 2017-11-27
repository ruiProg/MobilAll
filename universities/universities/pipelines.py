# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy.exceptions
import logging

#some universities may have campus in different cities
#website is a better id than name but not enough, universities alias need to be taken in account
class UniqueUniv(object):

	def __init__(self):
		self.univs = {}
		self.alias = {}

	def process_item(self, item, spider):
		if item['website'] in self.univs:
			values = self.univs[item['website']]
			if len(values) > 0 and 'city' not in item: #if there are cities set for university and only have country info
				raise scrapy.exceptions.DropItem("Duplicate item found: %s" % item)
			#university is invalid if for the same city, there is an entry with same name
			#same city, different name -> alias
			#different city -> different campus
			for city in values:
				if item['city'] == city:
					for name in self.alias[item['website']]:
						if item['name'] == name:
							logging.info("Repeated item:", item)
							raise scrapy.exceptions.DropItem("Duplicate item found: %s" % item)
			self.univs[item['website']].append(item['city'])
			self.alias[item['website']].append(item['name'])
			return item
		else:
			self.univs[item['website']] = [item['city']]
			self.alias[item['website']] = [item['name']]
			return item
