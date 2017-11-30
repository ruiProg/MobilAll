from flask import Blueprint, jsonify, request
import util, mobilAll, json

priceQueries_api = Blueprint('priceQueries_api', __name__)

#Item price queries

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

#list of prices of an item in a place
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
					{"match": {"itemName": {"query" : item, "fuzziness": "AUTO"}}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query" :{
								"multi_match" : {
									"query": place,
									"fuzziness": "AUTO",
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

#list of all item prices in a place
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
						"fuzziness": "AUTO",
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

#list of item prices for a category in a place
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
					{"match": {"category": {"query" : category, "fuzziness": "AUTO"}}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query" :{
								"multi_match" : {
									"query": place,
									"fuzziness": "AUTO",
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

#list of cities where certain item price is higher than certain value
@priceQueries_api.route('/api/itemPriceHigherThan')
def itemPriceHigherThanAverage():
	item = request.args.get('item', '')
	value = float(request.args.get('value', '0'))
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"itemName": {"query": item, "fuzziness": "AUTO"}}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query": {
								"match_all": {}
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]}
						}
					}
				],
				"filter" : [
				  {"range" : {"average_price" : {"gte" : value}}}
				  ]
			}
		}
    }
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#list of cities where certain item price is lower than certain value
@priceQueries_api.route('/api/itemPriceLowerThan')
def itemPriceLowerThanAverage():
	item = request.args.get('item', '')
	value = float(request.args.get('value', '0'))
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" : size,
		"query" : { 
			"bool" : {
				"must" : [
					{"match": {"itemName": {"query": item, "fuzziness": "AUTO"}}},
					{
						"has_parent" : {
							"parent_type": "region",
							"query": {
								"match_all": {}
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]}
						}
					}
				],
				"filter" : [
				  {"range" : {"average_price" : {"lte" : value}}}
				  ]
			}
		}
    }
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'

#Obtain places sorted by a item price
@priceQueries_api.route('/api/sortItemPrices')
def sortItemPrices():
	item = request.args.get('item', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" :size,
		"query" : { 
			"bool" : {
				"must" : [
					{"multi_match" : {
						"query": item,
						"fuzziness": "AUTO",
						"fields": ["itemName", "category"]
						}
					},
					{
						"has_parent" : {
							"parent_type": "region",
							"query": {
								"match_all": {}
							},
							"inner_hits": { "_source" : ["univRegion", "regionName"]}
						}
					}
				]
			}
		},
		"sort": [
		  {
		    "average_price": {
		      "order": "asc"
		    }
		  }
		]
	}
	res = util.es.search(index=util.pricesIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No item found'


#Check how reliable is the information about one city item prices
@priceQueries_api.route('/api/priceReliability')
def priceReliability():
	place = request.args.get('place', '')
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from" : offset, 
		"size" :size,
		"query" : {
			"bool" :{
				"must" : [
					{"multi_match": {
						"query" : place,
						"fuzziness": "AUTO",
						"fields" :  ["univRegion", "regionName"] }},
						{
							"has_child" : {
								"type": "price", 
								"query": {
									"match_all": {}
								}
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


