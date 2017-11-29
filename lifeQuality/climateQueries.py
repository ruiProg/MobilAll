from flask import Blueprint, jsonify, request
import util, mobilAll

climateQueries_api = Blueprint('climateQueries_api', __name__)
climateFactors = {
	"hail": "changeofhailday", 
	"snow" : "chanceofsnowonground",
	"tornado": "chanceoftornadoday",
	"rain" : "chanceofrainday",
	"fog" :  "chanceoffogday",
	"windy" : "chanceofwindyday",
	"thunder" : "chanceofthunderday",
	"sultry" : "chanceofsultryday",
	"cloudy" : "chanceofcloudyday",
	"sunnycloudy" : "chanceofsunnycloudyday",
	"partlycloudy" : "chanceofpartlycloudyday",
	"humid" : "chanceofhumidday",
	"precip" : "chanceofprecip"
}

#Climate queries

#find climate in a city
@climateQueries_api.route('/api/cityClimate')
def placeClimate():
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : {
			"has_parent" : {
				"parent_type": "city", 
				"query" :{
					"multi_match" : {
						"query": place,
						"fields": ["univRegion", "regionName"]
					}
				},
				"inner_hits": { "_source" : ["univRegion", "regionName"]} 
			}
		}
	}
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#find months in a city that have higher climate index than the threshold
@climateQueries_api.route('/api/climateBestMonths')
def climateBestMonths():
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	threshold = float(request.args.get('threshold', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{
						"has_parent" : {
							"parent_type": "city",
							"query": {
								"multi_match": {
								  "query" : place,
								"fields" :  ["univRegion", "regionName"] }
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]}
						}
					}
				],
				"filter" : [
					{"range" : {"climate_index" : {"gte" : threshold}}}
				]
			}
		}
    }
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#find climate in a city
@climateQueries_api.route('/api/sortedCityClimate')
def sortedCityClimate():
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query" : {
			"has_child" : {
				"type": "climate", 
				"query" : {
					"match_all": {}
				}
			}
		},
		"sort" : [ {"climate_index" : {"order" : "desc"}} ]
	}
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#find cities where certain month is within best months to visit
@climateQueries_api.route('/api/climateMonthBestCities')
def climateMonthBestCities():
	month = request.args.get('month','')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query" : {
			"match": {
		  		"best_months_to_visit_text": month
			}
		}
	}
	if nameSort > 0:
		query['sort'] = ["univRegion.keyword"]
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#Check which month, city pair have average temperatures between certain limits
@climateQueries_api.route('/api/temperatureLimits')
def temperatureLimits():
	month = request.args.get('month','')
	place = request.args.get('place','')
	minTemp = float(request.args.get('min', '0'))
	maxTemp = float(request.args.get('max', '0'))
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : {
		  "bool": {
		    "must": [{
    			"has_parent" : {
    				"parent_type": "city", 
    				"query" :{
    					"match_all": {}
    				},
    				"inner_hits": { "_source" : ["univRegion", "regionName"]}
    			}
		    }],
		    "filter": [
		      {"range" : {"temp_high_avg" : {"lte" : maxTemp}}},
		      {"range" : {"temp_low_avg" : {"gte" : minTemp}}}
		    ]
		  }
		}
	}
	if place:
		query['query']['bool']['must'][0]['has_parent']['query'] = {"match": { "regionName": place}}
	if month:
		query['query']['bool']['must'].append({"match" : {"month" : month}})
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#Highest temperature per city
@climateQueries_api.route('/api/highestTemperature')
def highestTemperature():
	nameSort = int(request.args.get('sort', '0'))
	maxCities = 2000
	query = {
		"size": 0,
		"aggs" : {
			"cities" : {
				"terms" : {
					"field" : "univRegion.keyword",
					"order": {
					   "to-climate>highest" : "desc"
					 },
					"size": maxCities
				},
				"aggs": {
				  	"to-climate": {
				    	"children": {
				    		"type": "climate"
				    	},
				    	"aggs": {
				    		"highest": {
				    			"max": {
				        			"field": "temp_high_max"
				        		}
				      		}
				    	}
				    }
				}
			}
		}
	}
	if nameSort > 0:
		query['aggs']['cities']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.climateIndex, body=query)
	return jsonify(res['aggregations']['cities']['buckets'])

#Lowest temperature per city
@climateQueries_api.route('/api/lowestTemperature')
def lowestTemperature():
	nameSort = int(request.args.get('sort', '0'))
	maxCities = 2000
	query = {
		"size": 0,
		"aggs" : {
			"cities" : {
				"terms" : {
					"field" : "univRegion.keyword",
					"order": {
					   "to-climate>lowest" : "asc"
					 },
					"size": maxCities
				},
				"aggs": {
				  	"to-climate": {
				    	"children": {
				    		"type": "climate"
				    	},
				    	"aggs": {
				    		"lowest": {
				    			"max": {
				        			"field": "temp_low_min"
				        		}
				      		}
				    	}
				    }
				}
			}
		}
	}
	if nameSort > 0:
		query['aggs']['cities']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.climateIndex, body=query)
	return jsonify(res['aggregations']['cities']['buckets'])

#Include, exclude factors
@climateQueries_api.route('/api/climateFactors')
def climateFactorsInOut():
	inclValues = request.args.getlist('include')
	exclValues = request.args.getlist('exclude')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : {
		  "bool": {
		    "must": [{
    			"has_parent" : {
    				"parent_type": "city", 
    				"query" :{
    					"match_all": {}
    				},
    				"inner_hits": { "_source" : ["univRegion", "regionName"]}
    			}
		    }],
		    "filter": [
		    ]
		  }
		}
	}
	for item in inclValues:
		if item in climateFactors:
			query['query']['bool']['filter'].append({"range" : {climateFactors[item] : {"gt" : 0}}})
	for item in exclValues:
		if item in climateFactors:
			query['query']['bool']['filter'].append({"range" : {climateFactors[item] : {"lte" : 0}}})
	res = util.es.search(index=util.climateIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'