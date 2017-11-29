from flask import Blueprint, jsonify, request
import util, mobilAll, json

indicesQueries_api = Blueprint('indicesQueries_api', __name__)

#Indices queries

#get place indices
@indicesQueries_api.route('/api/placeIndices')
def placeIndices():
	name = request.args.get('name', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"from" : offset,
		"size" : size,
		"query": {
			"multi_match": {
				"query": name,
				"fields": ["regionName", "univRegion"]
			}
		}
	}
	if nameSort > 0:
		query['sort'] = ["univRegion.keyword"]
	res = util.es.search(index=util.indicesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return "Place not found"