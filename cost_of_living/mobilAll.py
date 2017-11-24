from flask import Flask
from indexing import indexing_api
from queries import queries_api

app = Flask(__name__)
app.register_blueprint(indexing_api)
app.register_blueprint(queries_api)

@app.route('/')
def entry():
	return 'Dev mode'

if __name__ == "__main__":
	app.run()