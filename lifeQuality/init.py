from subprocess import Popen, CREATE_NEW_CONSOLE
import os, util, sys, socket
import indexing, mobilAll, mapping

def envDef():
	with open(util.configFile, 'r') as f:
		entries = f.read().splitlines()
		for entry in entries:
			key, value = entry.split('=')
			os.environ[key] = value
		os.environ[util.mobilAll] = os.path.dirname(os.getcwd())

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
os.chdir(os.path.dirname(os.path.abspath(__file__)))
envDef()
indexLifeQuality = False
if '-index' in sys.argv:
	indexing.deleteIndices()
	removeSincedb()
	removeDB()
	mobilAll.initDB()
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
Popen(['flask', 'run'], cwd=os.path.join(os.environ[util.mobilAll], util.lifeQuality))
#except:
#	print('Unexpected error reindexing')