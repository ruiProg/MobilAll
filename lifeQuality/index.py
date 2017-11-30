import util

def createUnivIndex():
	doc = {
		"settings": {
			"analysis": {
				"analyzer": {
					"default": {
						"tokenizer": "standard",
						"filter":  [ "standard", "lowercase", "asciifolding", "word_delimiter" ]
					}
				}
			}
		},
		"mappings": {
			"doc": {
				"properties": {
					"website": {
						"enabled": "false"
					}
				}
			}
		}
	}
	util.es.indices.create(index=util.univsIndex, body=doc)

def createFlowIndex():
	doc =  {
    	"mappings": {
        	"doc": {
            	"properties": {
                	"Value": {
                    	"type": "integer"
                	},
					"Time": {
                    	"type": "integer"
                	}
            	}
        	}
     	}
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
                	},
                	"dewpoint_high_min" : {
                		"enabled" : "false"
                	},
                	"dewpoint_high_avg" : {
                		"enabled" : "false"
                	},
                	"dewpoint_high_max" : {
                		"enabled" : "false"
                	},
                	"dewpoint_low_min" : {
                		"enabled" : "false"
                	},
                	"dewpoint_low_avg" : {
                		"enabled" : "false"
                	},
                	"dewpoint_low_max" : {
                		"enabled" : "false"
                	},
                	"chanceofsnowday" : {
                		"enabled" : "false"
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