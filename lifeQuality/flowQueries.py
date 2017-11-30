from flask import Blueprint, jsonify, request
import util, mobilAll, json

flowQueries_api = Blueprint('flowQueries_api', __name__)

#Flows queries

#General flow Trends
@flowQueries_api.route('/api/flowTrends')
def flowTrends():
	offset = int(request.args.get('from', '0'))
	size = int(request.args.get('size', util.defaultSize))
	query = {
		"from": offset,
		"size": size,
		"query" : { 
		  "match_all": {}
		},
		"sort": [
		  {
		    "Time": {
		      "order": "desc"
		    }
		  },
		  {
		    "Value" : {
		      "order" : "desc"
		    }
		  }
		]
	}
	res = util.es.search(index=util.flowsIndex, body=query)
	if res['hits']['hits']:
		return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
	else:
		return 'No trend found'


#Average count of people going from one country to another
@flowQueries_api.route('/api/averageFlow')
def averageFlow():
    orig = request.args.get('orig','')
    dest = request.args.get('dest','')
    query = {
        "size" : 0,
        "query" : {
            "bool": {
                "must": [
                    {  "match": { "To" : { "query" : dest, "fuzziness": "AUTO"} } },
                    {  "match": { "From" : {"query" : orig, "fuzziness": "AUTO"} } }
                ]
            }
        },
        "aggs" :{
            "average" : {
                "avg" : {
                    "field": "Value"
                }
            }
        }
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    return jsonify(res['aggregations']['average'])

#Incoming flow trends
@flowQueries_api.route('/api/incomingTrends')
def incomingTrends():
    country = request.args.get('country','')
    maxCountries = 250
    query = {
		"size" : 0,
        "query" : { 
            "match": {
                "To" : {"query": country, "fuzziness": "AUTO"}
            }
        },
        "aggs" :{
            "flows" : {
                "terms" : {
                    "field": "From.keyword",
                    "order": {
                        "average" : "desc"
                    },
                    "size" : maxCountries
                },
                "aggs":{
                    "average" :{
                        "avg" : {
                            "field" : "Value"
                        }
                    }
                }
            }
        }
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    return jsonify(res['aggregations']['flows']['buckets'])

#Outgoing flows trends
@flowQueries_api.route('/api/outgoingTrends')
def outgoingTrends():
    country = request.args.get('country','')
    maxCountries = 250
    query = {
		"size" : 0,
        "query" : { 
            "match": {
                "From" : {"query" : country, "fuzziness": "AUTO"}
            }
        },
        "aggs" :{
            "flows" : {
                "terms" : {
                    "field": "To.keyword",
                    "order": {
                        "average" : "desc"
                    },
                    "size" : maxCountries
                },
                "aggs":{
                    "average" :{
                        "avg" : {
                            "field" : "Value"
                        }
                    }
                }
            }
        }
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    return jsonify(res['aggregations']['flows']['buckets'])
	
#Total count of incoming students
@flowQueries_api.route('/api/totalIncoming')
def totalIncoming():
    country = request.args.get('country','')
    maxYears = 10
    query = {
        "size" : 0,
        "query" : { 
            "match": {
                "To" : {"query" : country, "fuzziness": "AUTO"}
            }
        },
        "aggs" :{
            "flows" : {
                "terms" : {
                    "field": "Time",
                    "order": {
                        "_key" : "desc"
                    },
                    "size" : maxYears
                },
                "aggs":{
                    "total" :{
                        "sum" : {
                            "field" : "Value"
                        }
                    }
                }
            }
        }
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    return jsonify(res['aggregations']['flows']['buckets'])

#Total count of outgoing students
@flowQueries_api.route('/api/totalOutgoing')
def totalOutgoing():
    country = request.args.get('country','')
    maxYears = 10
    query = {
        "size" : 0,
        "query" : { 
            "match": {
                "From" : {"query" : country, "fuzziness": "AUTO"}
            }
        },
        "aggs" :{
            "flows" : {
                "terms" : {
                    "field": "Time",
                    "order": {
                        "_key" : "desc"
                    },
                    "size" : maxYears
                },
                "aggs":{
                    "total" :{
                        "sum" : {
                            "field" : "Value"
                        }
                    }
                }
            }
        }
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    return jsonify(res['aggregations']['flows']['buckets'])

#Most recent entry from country to another
@flowQueries_api.route('/api/mostRecentEntry')
def mostRecentEntry():
    orig = request.args.get('orig','')
    dest = request.args.get('dest','')
    query = {
        "size" : 1,
        "query" : {
            "bool": {
                "must": [
                    {  "match": { "To" : { "query" : dest, "fuzziness": "AUTO"} } },
                    {  "match": { "From" : {"query" : orig, "fuzziness": "AUTO"} } }
                ]
            }
        },
        "sort": [
            {"Time": {
                "order": "desc"}
            }
        ]
    }
    res = util.es.search(index=util.flowsIndex, body=query)
    if res['hits']['hits']:
        return jsonify({"nbItems" : res['hits']['total'], "items": [item if util.debug else item['_source'] for item in res['hits']['hits']]})
    else:
        return "nothing found"
