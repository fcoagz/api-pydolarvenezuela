from flask import Flask, jsonify, request
from flask_cors import CORS

from src.obtaining import pyDolarVenezuelaApi
from src.exceptions import (
    forbidden,
    page_not_found,
    internal_server_error,
    gateway_timeout
)

api = pyDolarVenezuelaApi()
app = Flask(__name__)
CORS(app)

# error handling
app.register_error_handler(403, forbidden)
app.register_error_handler(404, page_not_found)
app.register_error_handler(500, internal_server_error)
app.register_error_handler(504, gateway_timeout)

@app.route('/')
def index():
    return "<p>Welcome to the Dolar Venezuela API. Go to documentation: https://github.com/fcoagz/api-pydolarvenezuela</p>"

@app.route('/api/v1/dollar/', methods=["GET"])
def get_monitors():
    response = jsonify(api.get_all_monitors())
    return response

@app.route('/api/v1/dollar/page', methods=["GET"])
def get_monitor_by_page_or_monitor():
    page    = request.args.get('page', None)
    monitor = request.args.get('monitor', None)

    if not page:
        return jsonify({'error': 'Por favor, proporciona el parametro: (page).'}), 400

    if monitor:
        response = jsonify(api.get_information_dollar(page, monitor))
    else:
        response = jsonify(api.get_specific_page_monitors(page))
    return response

@app.route('/api/v1/dollar/conversion', methods=["GET"])
def value_conversion():
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400

    response = jsonify(api.get_price_converted(type, value, monitor))
    return response

@app.route('/api/v1/dollar/unit/<string:key_monitor>', methods=["GET"])
def get_by_monitor(key_monitor: str):
    response = jsonify(api.get_information_dollar(monitor_code=key_monitor))
    return response

@app.route('/api/v1/dollar/history')
def get_prices_history():
    response = jsonify(api.get_price_history())
    return response