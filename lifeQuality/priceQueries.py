from flask import Blueprint, jsonify, request
import util, mobilAll, json

priceQueries_api = Blueprint('priceQueries_api', __name__)

#all items
@priceQueries_api.route('/api/items')
def items():
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	itList = [
		{
			"id" : row['id'],
			"rent" : row['rent'],
			"customer price index" : row['cpi'],
			"name" : row['itemName'],
			"category" : row['category'] 
		}
		for row in mobilAll.getItems()
	]
	return json.dumps(itList)

@priceQueries_api.route('/api/itemPricebyPlace')
def itemPricebyPlace():
	item = request.args.get('item', '')
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"itemName": item}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query" :{
								"multi_match" : {
								"query": place,
									"fields": ["univRegion", "regionName"]
								}
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]}
						}
					}
				]
			}
		}
    }
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

@priceQueries_api.route('/api/placePrices')
def placePrices():
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : {
			"has_parent" : {
				"parent_type": "region", 
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
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

@priceQueries_api.route('/api/categorybyPlace')
def categorybyPlace():
	category = request.args.get('category', '')
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"category": category}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query" :{
								"multi_match" : {
								"query": place,
									"fields": ["univRegion", "regionName"]
								}
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]} 
						}
					}
				]
			}
		}
	}
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

@priceQueries_api.route('/api/itemPriceHigherThanAverage')
def itemPriceHigherThanAverage():
	item = request.args.get('item', '')
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	average = float(request.args.get('average', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"itemName": item}},
					{
						"has_parent" : {
							"parent_type": "region",
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
				  {"range" : {"average_price" : {"gte" : average}}}
				  ]
			}
		}
    }
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

@priceQueries_api.route('/api/itemPriceLowerThanAverage')
def itemPriceLowerThanAverage():
	item = request.args.get('item', '')
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	average = float(request.args.get('average', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"itemName": item}},
					{
						"has_parent" : {
							"parent_type": "region",
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
				  {"range" : {"average_price" : {"lte" : average}}}
				  ]
			}
		}
    }
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'


