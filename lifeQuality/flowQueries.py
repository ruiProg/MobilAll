from flask import Blueprint, jsonify, request
import util, mobilAll, json

flowQueries_api = Blueprint('flowQueries_api', __name__)

#Indices queries

#all items