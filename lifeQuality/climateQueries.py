from flask import Blueprint, jsonify, request
import util, mobilAll

climateQueries_api = Blueprint('climateQueries_api', __name__)

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
