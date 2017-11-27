from subprocess import call
from flask import Blueprint
from elasticsearch import helpers
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys, os, requests, json, calendar, threading, time
import util, mobilAll

# check if city or country
# do API request with value['region']
# denormalize response
# index information to ES
def processValue(value):
	region = value['region']
	print("Processing {}".format(region))
	if value['cityFlag']:
		indexPrices('city_prices', 'query', region)
		indexIndices('indices', 'query', region)
		indexClimate(region)
	else:
		indexPrices('country_prices', 'country', region)
		indexIndices('country_indices', 'country', region)

def indexValue():
	with mobilAll.app.app_context():
		time.sleep(util.delay)
		nbTries = util.nbTries
		with util.lock:
			value = mobilAll.newEntryToProcess()
		while value is not None or nbTries > 0:
			if value is not None:
				processValue(value)
				nbTries = util.nbTries
			else:
				nbTries -= 1
				time.sleep(util.delay)
			with util.lock:
					value = mobilAll.newEntryToProcess()

def generateCityDoc(city):
	dic = {
		"_index": util.citiesIndex,
		"_type": util.defaultType,
		"_source": {
			"city": city['city'],
			"country": city['country'],
			"city_id": city['city_id']
		}
	}
	if 'latitude' in city and 'longitude' in city:
		dic['_source']['location'] = {
			"lat": city['latitude'],
			"lon": city['longitude']
		}
	return dic

def generatePriceDoc(item, parentID):
	dbItem = mobilAll.getItem(item['item_id'])
	dic = {
		"_index": util.pricesIndex,
		"_type": util.defaultType,
		"_source": {
			"item_id": item['item_id'],
			"rent": dbItem['rent'],
			"consumer_price_index": dbItem['cpi'],
			"itemName": dbItem['itemName'],
			"category": dbItem['category'],
			"regionPrice": {
				"name": "price",
				"parent": parentID
			},
			"average_price": item['average_price']
		}
	}

	if 'lowest_price' in item:
		dic['_source']['lowest_price'] = item['lowest_price']
	if 'highest_price' in item:
		dic['_source']['highest_price'] = item['highest_price']
	return dic

def generateClimateDoc(item, month, parentID):
	dic = {
		"_index": util.climateIndex,
		"_type": util.defaultType,
		"_source": item
	}
	dic['_source']['month'] = generateClimateDoc.months[month]
	dic['_source']['cityClimate'] = {
		"name": "climate",
		"parent": parentID
	}
	return dic

generateClimateDoc.months = dict((k,v) for k,v in enumerate(calendar.month_name))

#store items in sqlite3 db
def getItems():
	requestUrl = '{}/price_items?api_key={}'.format(util.apiUrl, util.apiKey)
	r = requests.get(requestUrl)
	data = json.loads(r.text)['items']
	with mobilAll.app.app_context():
		for item in data:
			mobilAll.createItem(item['item_id'], item['rent_factor'], item['cpi_factor'], item['name'], item['category'])
	print('Items retrieved')

def indexUnivs():
	util.univProc = Popen(['scrapy', 'crawl', 'univSpider'], creationflags=CREATE_NEW_CONSOLE, cwd=os.path.join(os.environ[util.mobilAll], util.universities))

def indexFlows():
	workDir = os.path.join(os.environ[util.logstash], 'bin')
	file = os.path.join(os.environ[util.mobilAll], *[util.flows, 'flows.conf'])
	Popen([os.path.join(workDir,'logstash.bat'), '-f', file], creationflags=CREATE_NEW_CONSOLE, cwd=workDir)

def indexCities():
	requestUrl = '{}/cities?api_key={}'.format(util.apiUrl, util.apiKey)
	r = requests.get(requestUrl)
	data = json.loads(r.text)['cities']
	actions = [
		generateCityDoc(city)
		for city in data
	]
	helpers.bulk(util.es, actions)
	print('Cities indexed')

#use scan abstraction of scroll in order to perform deep scrolling
#performance time in retrieving is actually 0, time spent within communication and processing
def indexLifeQuality():
	allUnivs = { 
		"query" : {
			"match_all" : {}
		}
	}
	res = helpers.scan(index=util.univsIndex, client=util.es, query=allUnivs)
	with mobilAll.app.app_context():
		util.threads = []
		for i in range(util.nbThreads):
			t = threading.Thread(target=indexValue)
			t.daemon = True
			util.threads.append(t)
			t.start()
		for i in res:
			city = i['_source']['city']
			country = i['_source']['country']
			if city and not mobilAll.existDBEntry(city, 1):
				mobilAll.createDBEntry(city, 1)
			if country and not mobilAll.existDBEntry(country, 0):
				mobilAll.createDBEntry(country, 0)

def indexPrices(queryType, paramType, name):
	requestUrl = '{}/{}?api_key={}&{}={}&currency={}'.format(util.apiUrl, queryType, util.apiKey, paramType, name, util.currency)
	r = requests.get(requestUrl)
	data = json.loads(r.text)
	if 'error' not in data and 'name' in data:
		doc = {
			"univRegion" : name,
			"regionName": data['name'],
			"monthLastUpdate": data['monthLastUpdate'],
			"yearLastUpdate": data['yearLastUpdate'],
			"contributors": data['contributors'],
			"regionPrice": {
				"name": "region"
			}
		}
		res = util.es.index(index=util.pricesIndex, doc_type=util.defaultType, body=doc)
		actions = [
			generatePriceDoc(item, res['_id'])
			for item in data['prices'] if 'average_price' in item
		]
		helpers.bulk(util.es, actions, routing=res['_id'])

def indexIndices(queryType, paramType, name):
	requestUrl = '{}/{}?api_key={}&{}={}'.format(util.apiUrl, queryType, util.apiKey, paramType, name)
	r = requests.get(requestUrl)
	data = json.loads(r.text)
	if 'error' not in data and 'name' in data:
		data['regionName'] = data['name']
		data['univRegion'] = name
		data.pop('name')
		util.es.index(index=util.indicesIndex, doc_type=util.defaultType, body=data)

def indexClimate(name):
	requestUrl = '{}/city_climate?api_key={}&query={}'.format(util.apiUrl, util.apiKey, name)
	r = requests.get(requestUrl)
	data = json.loads(r.text)
	if 'months' in data and 'name' in data:
		doc = {
			"univRegion" : name,
			"regionName": data['name'],
			"climate_index": data['climate_index'],
			"best_months_to_visit_text": data['best_months_to_visit_text'],
			"cityClimate": {
				"name": "city"
			}
		}
		res = util.es.index(index=util.climateIndex, doc_type=util.defaultType, body=doc)
		actions = [
			generateClimateDoc(item, int(month), res['_id'])
			for month, item in data['months'].items()
		]
		helpers.bulk(util.es, actions, routing=res['_id'])

def deleteIndices():
	util.es.indices.delete(index='*')
