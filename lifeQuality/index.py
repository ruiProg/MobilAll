import util

def createUnivIndex():
	doc = {
	"settings": {
			"analysis": {
				"analyzer": {
					"folding": {
						"tokenizer": "standard",
						"filter":  [ "lowercase", "asciifolding" ]
					}
				}
			}
		 },
		 "mappings": {
			"doc": {
				"properties": {
					"website": {
						"type": "text",
						"index": "false"
					}
				}
			}
		 }

	}
	util.es.indices.create(index=util.univsIndex, body=doc)

def createFlowIndex():
	doc = {

	}
	util.es.indices.create(index=util.flowsIndex, body=doc)

def createCityIndex():
	doc = {
    	"mappings": {
        	"doc": {
            	"properties": {
                	"location": {
                    	"type": "geo_point"
                	}
            	}
        	}
     	}
	}
	util.es.indices.create(index=util.citiesIndex, body=doc)

def createPriceIndex():
	doc = {
    	"mappings": {
        	"doc": {
            	"properties": {
                	"regionPrice": {
                    	"type": "join",
						"relations": {
							"region" : "price"
						}
                	}
            	}
        	}
     	}
	}
	util.es.indices.create(index=util.pricesIndex, body=doc)

def createIndiceIndex():
	doc = {

	}
	util.es.indices.create(index=util.indicesIndex, body=doc)

def createClimateIndex():
	doc = {
    	"mappings": {
        	"doc": {
            	"properties": {
                	"cityClimate": {
                    	"type": "join",
						"relations": {
							"city" : "climate"
						}
                	}
            	}
        	}
     	}
	}
	util.es.indices.create(index=util.climateIndex, body=doc)

def createIndices():
	createUnivIndex()
	createFlowIndex()
	createCityIndex()
	createPriceIndex()
	createIndiceIndex()
	createClimateIndex()