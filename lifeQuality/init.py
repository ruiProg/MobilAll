from subprocess import Popen, CREATE_NEW_CONSOLE
import os, util, sys, socket
import indexing, mobilAll

def envDef():
	with open(util.configFile, 'r') as f:
		entries = f.read().splitlines()
		for entry in entries:
			key, value = entry.split('=')
			os.environ[key] = value
		appFolder = os.path.dirname(os.path.abspath(__file__))
		os.environ[util.mobilAll], _ = os.path.split(appFolder)

def removeSincedb():
	folder = os.path.join(os.environ[util.logstash], *util.sincedb)
	for file in os.listdir(folder):
		path = os.path.join(folder, file)
		try:
			if os.path.isfile(path):
				os.unlink(path)
		except:
			print('Cannot remove logstash log file')

def removeDB():
	try:
		os.unlink(mobilAll.database)
	except:
		print('Cannot remove database')

def runKibana():
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((util.localhost,util.kibanaPort))
	if result == 0:
		print('Kibana is already is running')
	else:
		Popen([os.environ[util.kibana]], creationflags=CREATE_NEW_CONSOLE)

#try:
envDef()
indexLifeQuality = False
if '-i' in sys.argv:
	indexing.deleteIndices()
	removeSincedb()
	removeDB()
	mobilAll.initDB()
	indexing.createMappings()
	indexing.indexUnivs()
	indexing.indexFlows()
	indexing.getItems()
	indexing.indexCities()
	indexLifeQuality = True
if indexLifeQuality or '-l' in sys.argv:
	if util.univProc is not None:
		print("Waiting for universities indexing")
		util.univProc.wait()
	indexing.indexLifeQuality()
if '-k' in sys.argv:
	runKibana()
#except:
#	print('Unexpected error reindexing')