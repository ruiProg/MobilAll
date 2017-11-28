from subprocess import Popen, CREATE_NEW_CONSOLE
import os, util, sys, socket
import indexing, mobilAll, mapping

#read environment variables to be set through configuration file
#set parent folder from current working direcory as environment variable necessary in Logstash
def envDef():
	with open(util.configFile, 'r') as f:
		entries = f.read().splitlines()
		for entry in entries:
			key, value = entry.split('=')
			os.environ[key] = value
		os.environ[util.mobilAll] = os.path.dirname(os.getcwd())

#remove files that block reindexing student flows through Logstash
def removeSincedb():
	folder = os.path.join(os.environ[util.logstash], *util.sincedb)
	if os.path.exists(folder):
		for file in os.listdir(folder):
			path = os.path.join(folder, file)
			try:
				if os.path.isfile(path):
					os.unlink(path)
			except:
				print('Cannot remove logstash log file')

#remove sqlite3 db containing progress and list of items
def removeDB():
	try:
		os.unlink(mobilAll.database)
	except:
		print('Cannot remove database')

#check if Kibana is already running, if not open Kibana
def runKibana():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((util.localhost,util.kibanaPort))
	if result == 0:
		print('Kibana is already is running')
	else:
		Popen([os.environ[util.kibana]], creationflags=CREATE_NEW_CONSOLE)

try:
	#update working directory
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	#set environment variables
	envDef()
	indexLifeQuality = False
	if '-index' in sys.argv:
		#remove everything before indexing
		indexing.deleteIndices()
		removeSincedb()
		removeDB()
		#start sqlite3 db
		mobilAll.initDB()
		#create the indexing mapping
		mapping.createMappings()
		indexing.indexUnivs()
		indexing.indexFlows()
		indexing.getItems()
		indexing.indexCities()
		indexLifeQuality = True
	if indexLifeQuality or '-lifeQuality' in sys.argv:
		if util.univProc is not None:
			print("Waiting for universities indexing")
			util.univProc.wait()
		indexing.indexLifeQuality()
	if '-kibana' in sys.argv:
		runKibana()
	#wait for threads
	for t in util.threads:
		t.join()
	#run the server
	Popen(['flask', 'run'], cwd=os.path.join(os.environ[util.mobilAll], util.lifeQuality))
except:
	print('Unexpected error reindexing')