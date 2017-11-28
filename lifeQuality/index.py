import util

def createUnivIndex():
	doc = {

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

	}
	util.es.indices.create(index=util.pricesIndex, body=doc)

def createIndiceIndex():
	doc = {

	}
	util.es.indices.create(index=util.indicesIndex, body=doc)

def createClimateIndex():
	doc = {

	}
	util.es.indices.create(index=util.climateIndex, body=doc)

def createIndices():
	createUnivIndex()
	createFlowIndex()
	createCityIndex()
	createPriceIndex()
	createIndiceIndex()
	createClimateIndex()