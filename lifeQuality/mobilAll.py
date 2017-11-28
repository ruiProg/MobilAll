from flask import Flask, g
from geoQueries import geoQueries_api
from priceQueries import priceQueries_api
from climateQueries import climateQueries_api
import sqlite3, os
import util

database = os.path.join(os.path.dirname(os.path.abspath(__file__)), util.dbSrc)
app = Flask(__name__)
app.register_blueprint(geoQueries_api)
app.register_blueprint(priceQueries_api)
app.register_blueprint(climateQueries_api)

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

def generalQuery(query, args=()):
    cur = getDB().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None)

def selectAllQuery(query, args=()):
	cur = getDB().execute(query, args)
	rv = cur.fetchall()
	cur.close()
	return (rv if rv else None)

def existDBEntry(region, cityFlag):
	return generalQuery('SELECT id FROM entry WHERE region=? AND cityFlag=?', (region, cityFlag)) != None

def newEntryToProcess():
	value = generalQuery('SELECT id, region, cityFlag FROM entry WHERE done=0 ORDER BY id LIMIT 1')
	if value is not None:
		updateDBEntry(value['id'], 1)
	return value

def getEntry(id):
	return generalQuery('SELECT id, region, cityFlag FROM entry WHERE id=?', (id,))

def createDBEntry(region, cityFlag, done=0):
	db = getDB()
	db.cursor().execute('INSERT INTO entry(region, cityFlag, done) VALUES(?,?,?)', (region, cityFlag, done))
	db.commit()

def updateDBEntry(id, done):
	db = getDB()
	db.cursor().execute('UPDATE entry SET done=? WHERE id=?', (done, id))
	db.commit()

def createItem(id, rent, cpi, name, category):
	db = getDB()
	db.cursor().execute('INSERT INTO item(id, rent, cpi, itemName, category) VALUES(?,?,?,?,?)', (id, rent, cpi, name, category))
	db.commit()

def getItem(id):
	return generalQuery('SELECT id, rent, cpi, itemName, category FROM item WHERE id=?', (id,))

def getItems():
    return selectAllQuery('SELECT id, rent, cpi, itemName, category FROM item')

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
