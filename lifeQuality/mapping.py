import util

def createCityMapping():
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

def createMappings():
	createCityMapping()