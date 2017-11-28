from flask import Blueprint, jsonify, request
import util

univQueries_api = Blueprint('univQueries_api', __name__)

@univQueries_api.route('/api/universities')
def universityList():
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match_all": {}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "University is not found"
		
@univQueries_api.route('/api/university')
def findUniversity():
	name = request.args.get('name', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"name": name
			}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "University is not found"	
		
@univQueries_api.route('/api/univInCity')
def findUniversitiesInCity():
	city = request.args.get('city', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {
				"city": city
			}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university is found in " + city 	
		
@univQueries_api.route('/api/univInState')
def findUniversitiesInState():
	state = request.args.get('state', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {"country": "United States"},
			"match": {"state": state}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university is found in state of" + state
		
@univQueries_api.route('/api/univInCountry')
def findUniversitiesInCountry():
	country = request.args.get('country', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"match": {"country": country}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "No university is found in" + country
		
@univQueries_api.route('/api/univOnCampus')
def findUniversitiesOnCampus():
	name = request.args.get('name', '')
	country = request.args.get('country', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query": {
			"bool": {
				"must": [
					{"match": { "country": country}},
					{"match": { "name": name}}
				]
			}
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return name + " is not found in " + country
		
@univQueries_api.route('/api/searchAll')
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
				"fields": ["name", "city", "website", "state", "country"]
			}	
		}		
	}
	res = util.es.search(index=util.univsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return input + " is not found"