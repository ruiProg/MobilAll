from flask import Blueprint, jsonify, request
import util

geoQueries_api = Blueprint('geoQueries_api', __name__)

#Geographical queries

#list of countries with universities
#optimize query with size: 0
#average time with hits: 4ms
#average time without hits: 2ms
@geoQueries_api.route('/api/countries')
def countriesList():
	maxCountries = 250
	nameSort = int(request.args.get('sort', '0'))
	print(nameSort)
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
	if nameSort > 0:
		query['aggs']['countries']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.univsIndex, body=query)
	return jsonify(res['aggregations']['countries'][util.aggList])

#list of cities with universities
#optimize query with size: 0
#average time with hits: 35ms
#average time without hits: 25ms
@geoQueries_api.route('/api/cities')
def citiesList(nameSort=False):
	maxCities = 4000
	nameSort = int(request.args.get('sort', '0'))
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
	if nameSort > 0:
		query['aggs']['cities']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.univsIndex, body=query)
	return jsonify(res['aggregations']['cities'][util.aggList])


@geoQueries_api.route('/api/states')
def statesList(nameSort=False):
	maxStates = 60
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"size": 0,
		"aggs" : {
			"states" : {
				"terms" : {
					"field" : "state.keyword",
					"size": maxStates
				}
			}
		}
	}
	if nameSort > 0:
		query['aggs']['states']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.univsIndex, body=query)
	return jsonify(res['aggregations']['states'][util.aggList])
