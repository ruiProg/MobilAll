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
	countTag = 'count'
	cityTag = 'city'
	domTag = 'dom'
	regionTag = 'region'
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
					self.domTag: value, #US or world region
					self.countTag: count, #nb of universities in country/state
					self.regionTag: region #name of country/state
					})


	def parseCities(self, response):
		for item in response.xpath('//option'):
			value = item.xpath('@value').extract_first()
			if value: #sometimes first value is invalid, but not always
				_, cityName = parseItem(item)
				#add city name to metadata
				nextMeta = response.meta
				nextMeta[self.cityTag] = cityName
				yield scrapy.Request(self.cityUrl.format(value), callback=self.parseUnivs, meta=nextMeta)
		#some universities don't have a corresponding city information, obtain only the country
		nextMeta = response.meta
		nextMeta[self.cityTag] = ''
		#iterate for every page with low priority in order to process universities with cities first
		#duplicated university check in pipelines
		acc = self.startIndex
		while acc < response.meta[self.countTag]:
			yield scrapy.Request(self.domPagedUrl.format(response.meta[self.domTag], acc), callback=self.parseUnivs, meta=nextMeta, priority=self.priorityLevel)
			acc += self.itemsPerPage

	def parseUnivs(self, response):
		for item in response.xpath('//td/ol/li/a'):
			univ = UnivItem()
			univ['name'] = item.xpath('text()').extract_first() #not unique, some countries may have universities with same name
			univ['website'] = item.xpath('@href').extract_first() #domain restriction allows to better determine a university through a single field
			univ['city'] = response.meta[self.cityTag]
			if response.meta[self.domTag].startswith(self.usIdentifier): #regions starting with edu_ belong to US
				univ['country'] = self.usName
				univ['state'] = response.meta[self.regionTag]
			else:
				univ['country'] = response.meta[self.regionTag]
				univ['state'] = ''
			yield univ
