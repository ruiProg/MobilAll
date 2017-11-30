from flask import Blueprint, jsonify, request
import util

univQueries_api = Blueprint('univQueries_api', __name__)

# University queries

# list all universities
@univQueries_api.route('/api/universities')
def universityList():
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match_all": {}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "University not found"
		
#find university by name		
@univQueries_api.route('/api/university')
def findUniversity():
	name = request.args.get('name', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"name": name
			}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "University not found"	
	
#find the list universities in one city		
@univQueries_api.route('/api/cityUnivs')
def findUniversitiesInCity():
	city = request.args.get('city', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"city": {"query" : city, "fuzziness": "AUTO"}
			}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university found in " + city 	
		
#find the list universities in one state	
@univQueries_api.route('/api/stateUnivs')
def findUniversitiesInState():
	state = request.args.get('state', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {"country": "United States"},
			"match": {"state": {"query" : state, "fuzziness": "AUTO"}}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university found in state of " + state
		
#find the list universities in one country		
@univQueries_api.route('/api/countryUnivs')
def findUniversitiesInCountry():
	country = request.args.get('country', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {"country": {"query": country, "fuzziness": "AUTO"}}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university found in " + country
		
#find the list of campus of a university (logic behind: a university with same name and in the same country can have multiple campus)
@univQueries_api.route('/api/univOnCampus')
def findUniversitiesOnCampus():
	name = request.args.get('name', '')
	country = request.args.get('country', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"bool": {
				"must": [
					{"match": { "country": {"query": country, "fuzziness": "AUTO"}}},
					{"match": { "name": {"query": name, "fuzziness": "AUTO"}}}
				]
			}
		}		
	}
	if nameSort > 0:
		query['sort'] = ["name.keyword"]
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return name + " not found in " + country
		
#general query, searching on all fields
@univQueries_api.route('/api/univSearchAll')
def searchAll():
	input = request.args.get('input', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"multi_match": {
				"query": input,
				"fuzziness": "AUTO",
				"fields": ["name", "city", "website", "state", "country"]
			}	
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return input + " not found"
		