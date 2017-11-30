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
                	},
                    "contributors" : {
                        "enabled" : "false"
                    },
                    "yearLastUpdate" : {
                        "enabled" : "false"
                    },
                    "monthLastUpdate": {
                        "enabled" : "false"
                    },
                    "highest_price": {
                        "enabled" : "false"
                    },
                    "lowest_price": {
                        "enabled" : "false"
                    }
            	}
        	}
     	}
	}
	util.es.indices.create(index=util.pricesIndex, body=doc)

def createIndiceIndex():
	doc = {
        "mappings": {
            "doc": {
                "properties": {
                    "property_price_to_income_ratio" : {
                        "enabled" : "false"
                    },
                    "traffic_inefficiency_index" : {
                        "enabled" : "false"
                    }
                }
            }
        }
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