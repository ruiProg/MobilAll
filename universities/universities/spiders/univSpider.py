import scrapy
from universities.items import UnivItem

# e.g. Lisbon (2) -> 2, Lisbon
def parseItem(item):
	itemText = item.xpath('text()').extract_first()
	delimiterPos = itemText.rfind(' ')
	return int(itemText[delimiterPos + 2 : -1]), itemText[:delimiterPos]


class UnivSpider(scrapy.Spider):
	name = 'univSpider'
	allowed_domains = ['univ.cc']
	start_urls = [
		'https://univ.cc/world.php',
		'https://univ.cc/states.php'
	]
	domUrl = 'https://univ.cc/search.php?dom={}'
	domPagedUrl = 'https://univ.cc/search.php?dom={}&key=&start={}'
	cityUrl = 'https://univ.cc/search.php?town={}'
	startIndex = 1
	itemsPerPage = 50
	priorityLevel = -5
	usIdentifier = 'edu'
	usName = 'United States'


	def parse(self, response):
		for index, item in enumerate(response.xpath('//option')):
			value = item.xpath('@value').extract_first()
			if index != 0: #first value is invalid
				count, region = parseItem(item)
				yield scrapy.Request(self.domUrl.format(value), callback=self.parseCities, 
					meta={ 
					'dom': value, #US or world region
					'count': count, #nb of universities in country/state
					'region': region #name of country/state
					})


	def parseCities(self, response):
		for item in response.xpath('//option'):
			value = item.xpath('@value').extract_first()
			if value: #sometimes first value is invalid, but not always
				_, cityName = parseItem(item)
				#add city name to metadata
				nextMeta = response.meta
				nextMeta['city'] = cityName
				yield scrapy.Request(self.cityUrl.format(value), callback=self.parseUnivs, meta=nextMeta)
		#some universities don't have a corresponding city information, obtain only the country
		nextMeta = response.meta
		nextMeta['city'] = '' #clear value
		#iterate for every page with low priority assigned in order to process universities with cities first
		#duplicated university check is done in pipelines
		acc = self.startIndex
		while acc < response.meta['count']:
			yield scrapy.Request(self.domPagedUrl.format(response.meta['dom'], acc), callback=self.parseUnivs, meta=nextMeta, priority=self.priorityLevel)
			acc += self.itemsPerPage

	def parseUnivs(self, response):
		for item in response.xpath('//td/ol/li/a'):
			univ = UnivItem()
			univ['name'] = item.xpath('text()').extract_first() #not unique, some countries may have universities with same name
			univ['website'] = item.xpath('@href').extract_first() #domain restriction allows to better determine a university through a single field
			if response.meta['city']:
				univ['city'] = response.meta['city']
			if response.meta['dom'].startswith(self.usIdentifier): #regions starting with edu_ belong to US
				univ['country'] = self.usName
				univ['state'] = response.meta['region']
			else:
				univ['country'] = response.meta['region']
			yield univ
