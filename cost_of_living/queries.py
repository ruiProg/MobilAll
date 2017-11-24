from flask import Blueprint, jsonify
import globalVal

queries_api = Blueprint('queries_api', __name__)

#Geographical queries

#list of countries with universities
#optimize query with size: 0
#average time with hits: 6ms
#average time without hits: 3ms
@queries_api.route('/api/countries')
def countiesList():
	maxCountries = 250
	query = {
		"size": 0, #don't retrieve hits
		"aggs" : {
			"countries" : {
				"terms" : {
					"field" : "country.keyword",
					"size": maxCountries
				}
			}
		}
	}
	res = globalVal.es.search(index=globalVal.univsIndex, body=query)
	return jsonify(res['aggregations']['countries'][globalVal.aggList])

#list of cities with universities
#optimize query with size: 0
#average time with hits: 60ms
#average time without hits: 40ms
@queries_api.route('/api/cities')
def citiesList():
	maxCities = 4000
	query = {
		"size": 0,
		"aggs" : {
			"cities" : {
				"terms" : {
					"field" : "city.keyword",
					"size": maxCities
				}
			}
		}
	}
	res = globalVal.es.search(index=globalVal.univsIndex, body=query)
	return jsonify(res['aggregations']['cities'][globalVal.aggList])