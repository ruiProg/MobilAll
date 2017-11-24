from flask import Blueprint
from elasticsearch import helpers
import globalVal

indexing_api = Blueprint('indexing_api', __name__)

#use scan abstraction of scroll in order to perform deep scrolling
#performance time in retrieving is actually 0, time spent within communication and processing
@indexing_api.route('/indexInfo')
def indexTask():
	allUnivs = { 
		"query" : {
			"match_all" : {}
		}
	}
	res = helpers.scan(index=globalVal.univsIndex, client=globalVal.es, query=allUnivs)
	for i in res:
		print(i['_source'])
	return "Indexing successful"
