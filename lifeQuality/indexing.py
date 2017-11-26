from subprocess import call
from flask import Blueprint
from elasticsearch import helpers
from subprocess import Popen, CREATE_NEW_CONSOLE
import sys, os, requests, json
import util, mobilAll

def createMappings():
	pass

def processValue(value):
	print("Processing {}".format(value['region']))
	# check if city or country
	# do API request with value['region']
	# denormalize response
	# index information to ES
	mobilAll.updateDBEntry(value['id'], 1)

def indexUnivs():
	util.univProc = Popen(['scrapy', 'crawl', 'univSpider'], creationflags=CREATE_NEW_CONSOLE, cwd=os.path.join(os.environ[util.mobilAll], util.universities))

def indexFlows():
	workDir = os.path.join(os.environ[util.logstash], 'bin')
	file = os.path.join(os.environ[util.mobilAll], *[util.flows, 'flows.conf'])
	Popen([os.path.join(workDir,'logstash.bat'), '-f', file], creationflags=CREATE_NEW_CONSOLE, cwd=workDir)

def indexCities():
	requestUrl = 'http://www.numbeo.com:8008/api/cities?api_key={}'.format(util.apiKey)
	r = requests.get(requestUrl)
	data = json.loads(r.text)['cities']
	actions = [
	{
		"_index": 'mobil_cities',
		"_type": 'doc',
		"_source": {
			"city": city['city'],
			"country": city['country'],
			"city_id": city['city_id'],
				"location" : {
					"lat": city['latitude'],
					"lon": city['longitude']
				}
		}
	}
	if 'latitude' in city and 'longitude' in city
	else 
	{
		"_index": 'mobil_cities',
		"_type": 'doc',
		"_source": {
			"city": city['city'],
			"country": city['country'],
			"city_id": city['city_id']
		}
	}
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
		for i in res:
			city = i['_source']['city']
			country = i['_source']['country']
			if city and not mobilAll.existDBEntry(city, 1):
				mobilAll.createDBEntry(city, 1)
			if country and not mobilAll.existDBEntry(country, 0):
				mobilAll.createDBEntry(country, 0)
			print('Checking {} : {}'.format(city if city else '_', country))
		value = mobilAll.newEntryToProcess()
		while value is not None:
			processValue(value)
			value = mobilAll.getEntry(value['id'] + 1)

def deleteIndices():
	util.es.indices.delete(index='*')
