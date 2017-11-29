from flask import Blueprint, jsonify, request
import util, mobilAll, json

indicesQueries_api = Blueprint('indicesQueries_api', __name__)
indexFactors = {
	"crime": "crime_index", 
	"traffictime" : "traffic_time_index",
	"cpirent": "cpi_and_rent_index",
	"purchasingpower" : "purchasing_power_incl_rent_index",
	"restaurant" :  "restaurant_price_index",
	"safety" : "safety_index",
	"co2" : "traffic_co2_index",
	"cpi" : "cpi_index",
	"quality" : "quality_of_life_index",
	"rent" : "rent_index",
	"healthcare" : "health_care_index",
	"traffic" : "traffic_index",
	"groceries" : "groceries_index",
	"pollution" : "pollution_index"
}

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

#Sort by index
@indicesQueries_api.route('/api/sortIndices')
def sortIndices():
	sortVal = request.args.get('sortVal', '0')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : {
			"match_all" : {}
		}
	}
	if sortVal in indexFactors:
		query['sort'] = {indexFactors[sortVal] : {"order" : "desc"}}
	print(query)
	res = util.es.search(index=util.indicesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'