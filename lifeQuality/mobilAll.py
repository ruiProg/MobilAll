from flask import Flask, g
from queries import queries_api
import sqlite3, os
import util

database = os.path.join(os.path.dirname(os.path.abspath(__file__)), util.dbSrc)
app = Flask(__name__)
app.register_blueprint(queries_api)

def getDB():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(database)
	db.row_factory = sqlite3.Row
	return db

def initDB():
	with app.app_context():
		db = getDB()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

def generalQuery(query, args=(), one=False):
    cur = getDB().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def existDBEntry(region, cityFlag):
	return generalQuery('SELECT id FROM entry WHERE region=? AND cityFlag=?', (region, cityFlag), True) != None

def newEntryToProcess():
	return generalQuery('SELECT id, region, cityFlag FROM entry WHERE done=0 ORDER BY id LIMIT 1', one=True)

def getEntry(id):
	return generalQuery('SELECT id, region, cityFlag FROM entry WHERE id=?', (id,), True)

def createDBEntry(region, cityFlag, done=0):
	db = getDB()
	db.cursor().execute('INSERT INTO entry(region, cityFlag, done) VALUES(?,?,?)', (region, cityFlag, done))
	db.commit()

def updateDBEntry(id, done):
	db = getDB()
	db.cursor().execute('UPDATE entry SET done=? WHERE id=?', (done, id))
	db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def entry():
	return 'Dev mode'

if __name__ == "__main__":
	app.run()
