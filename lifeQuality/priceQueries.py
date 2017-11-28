from flask import Blueprint, jsonify, request
import util

priceQueries_api = Blueprint('priceQueries_api', __name__)

#all items
@priceQueries_api.route('/api/items')
def items():
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
		return 'No item found'