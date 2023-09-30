from flask import Flask, jsonify
from flask_cors import CORS

from src.obtaining import NewApi
from src.exceptions import page_not_found, internal_server_error

api = NewApi()
app = Flask(__name__)
CORS(app)

# error handling
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)

@app.route('/')
def index():
    return "<p>Welcome to the Dolar Venezuela API. Go to documentation: https://github.com/fcoagz/api-pydolarvenezuela</p>"

@app.route('/api/v1/dollar/', methods=["GET"])
def get_monitors():
    response = jsonify(api.get_all_monitors())
    return response

@app.route('/api/v1/dollar/unit/<string:key_monitor>', methods=["GET"])
def get_by_monitor(key_monitor: str):
    response = jsonify(api.get_information_dollar(key_monitor))
    return response

@app.route('/api/v1/dollar/tb/<string:value>/<string:key_monitor>', methods=["GET"])
def convertion_to_dollar(value: str, key_monitor: str):
    response = jsonify(api.get_price_converted('VES', value, key_monitor))
    return response
    
@app.route('/api/v1/dollar/td/<string:value>/<string:key_monitor>', methods=["GET"])
def convertion_to_bs(value: str, key_monitor: str):
    response = jsonify(api.get_price_converted('USD', value, key_monitor))
    return response