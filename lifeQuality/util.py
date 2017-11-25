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
dbSrc = 'indexProgress.db'

es = Elasticsearch()


'''
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
'''