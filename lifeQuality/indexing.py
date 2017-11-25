from subprocess import call
from flask import Blueprint
from elasticsearch import helpers
from subprocess import Popen, CREATE_NEW_CONSOLE
import util
import sys
import os

def createMappings():
	pass

def indexUnivs():
	Popen(['scrapy', 'crawl', 'univSpider'], creationflags=CREATE_NEW_CONSOLE, cwd=os.path.join(os.environ[util.mobilAll], util.universities))

def indexFlows():
	workDir = os.path.join(os.environ[util.logstash], 'bin')
	file = os.path.join(os.environ[util.mobilAll], *[util.flows, 'flows.conf'])
	Popen([os.path.join(workDir,'logstash.bat'), '-f', file], creationflags=CREATE_NEW_CONSOLE, cwd=workDir)

#use scan abstraction of scroll in order to perform deep scrolling
#performance time in retrieving is actually 0, time spent within communication and processing
def indexNumbeo():
	allUnivs = { 
		"query" : {
			"match_all" : {}
		}
	}
	res = helpers.scan(index=util.univsIndex, client=util.es, query=allUnivs)
	for i in res:
		print(i['_source'])

def deleteIndices():
	util.es.indices.delete(index='*')
