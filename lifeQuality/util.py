from elasticsearch import Elasticsearch
import os

mobilAll = 'MOBIL_ALL'
logstash = 'LOGSTASH'
kibana = 'KIBANA'
lifeQuality = 'lifeQuality'
universities = 'universities'
flows = 'mobilityFlows'
sincedb = ['data', 'plugins', 'inputs', 'file']

univsIndex = 'mobil_univs'
aggList = 'buckets'

apiKey = 'k5vqn17p7o1ono'
localhost = '127.0.0.1'
kibanaPort = 5601
configFile = 'config.txt'
dbSrc = 'indexProgress.db3'

es = Elasticsearch()
univProc = None
