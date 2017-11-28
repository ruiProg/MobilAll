from elasticsearch import Elasticsearch
from threading import Lock
import os

mobilAll = 'MOBIL_ALL'
logstash = 'LOGSTASH'
kibana = 'KIBANA'
lifeQuality = 'lifeQuality'
universities = 'universities'
flows = 'mobilityFlows'
sincedb = ['data', 'plugins', 'inputs', 'file']

univsIndex = 'mobil_univs'
flowsIndex = 'mobil_flows'
citiesIndex = 'mobil_cities'
pricesIndex = 'mobil_prices'
indicesIndex = 'mobil_indices'
climateIndex = 'mobil_climate'
defaultType = 'doc'

apiUrl = 'http://www.numbeo.com:8008/api'
apiKey = 'k5vqn17p7o1ono'
localhost = '127.0.0.1'
kibanaPort = 5601
configFile = 'config.txt'
dbSrc = 'indexProgress.db3'
currency = 'EUR'
distanceUnit = 'Km'
defaultSize = 10

threads = []
nbThreads = 10
nbTries = 3
delay = 5
quit = False

es = Elasticsearch()
lock = Lock()
univProc = None
debug = True
