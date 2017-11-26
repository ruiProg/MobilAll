import os
from elasticsearch import Elasticsearch

mobilAll = 'MOBIL_ALL'
logstash = 'LOGSTASH'
kibana = 'KIBANA'
lifeQuality = 'lifeQuality'
universities = 'universities'
flows = 'mobilityFlows'
sincedb = ['data', 'plugins', 'inputs', 'file']

univsIndex = 'mobil_univs'
aggList = 'buckets'

localhost = '127.0.0.1'
kibanaPort = 5601
configFile = 'config.txt'
dbSrc = 'indexProgress.db3'

es = Elasticsearch()
