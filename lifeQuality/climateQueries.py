from flask import Blueprint, jsonify, request
import util, mobilAll

climateQueries_api = Blueprint('climateQueries_api', __name__)

Climate queries

#
@climateQueries_api.route('/api/cityClimate')
def countriesList():
	maxCountries = 250
	nameSort = int(request.args.get('sort', '0'))
	query = {
		"size": 0, #don't retrieve hits
		"aggs" : {
			"countries" : {
				"terms" : {
					"field" : "country.keyword",
					"size": maxCountries
				}
			}
		}
	}
	if nameSort > 0:
		query['aggs']['countries']['terms']['order'] = { "_key" : "asc" }
	res = util.es.search(index=util.univsIndex, body=query)
	return jsonify(res['aggregations']['countries']['buckets'])
