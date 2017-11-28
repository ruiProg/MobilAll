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
	return jsonify(res['aggregations']['countries']['buckets'])

#list of cities with universities
#optimize query with size: 0
#average time with hits: 35ms
#average time without hits: 25ms
@geoQueries_api.route('/api/cities')
def citiesList():
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
	return jsonify(res['aggregations']['cities']['buckets'])

#list of states with universities
@geoQueries_api.route('/api/states')
def statesList():
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
	return jsonify(res['aggregations']['states']['buckets'])

#list of cities in one country
@geoQueries_api.route('/api/countryCities')
def countryCities():
	name = request.args.get('country', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"country": name
			}
		}
	} 
	res = util.es.search(index=util.citiesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No city found'

#list of cities in one state
@geoQueries_api.route('/api/stateCities')
def stateCities():
	name = request.args.get('state', '')
	maxCities = 250
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"size": 0,
		"query": {
		  "match": {
		    "state": name
		  }
		}, 
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
	if res['aggregations']['cities']['buckets']:
		return jsonify(res['aggregations']['cities']['buckets'])
	else:
		return 'No city found'

#find city
@geoQueries_api.route('/api/city')
def city():
	name = request.args.get('name', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"city": name
			}
		}
	} 
	res = util.es.search(index=util.citiesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No city found'

#find close cities to a certain point
@geoQueries_api.route('/api/closeCities')
def closeCities():
	latVar = float(request.args.get('lat', '0.0'))
	lonVar = float(request.args.get('lon', '0.0'))
	print(lonVar)
	distance = float(request.args.get('distance', '10.0'))
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
	    "query": {
	        "bool" : {
	            "must" : {
	                "match_all" : {}
	            },
	            "filter" : {
	                "geo_distance" : {
	                    "distance" : str(distance)+"km",
	                    "location" : {
	                        "lat" : latVar,
	                        "lon" : lonVar
	                    }
	                }
	            }
	        }
	    },
	    "sort" : [
	    {
	    	"_geo_distance" : {
	    		"location" : {
	    			"lat" : latVar,
	    			"lon" : lonVar
	    		},
	    		"order" : "asc",
	    		"unit" : "km",
	    		"mode" : "min"
	    	}
	    }]
	}
	res = util.es.search(index=util.citiesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No city found'
