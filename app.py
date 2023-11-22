from flask import Flask, jsonify, request
from flask_cors import CORS

from src.exceptions import (
    forbidden,
    page_not_found,
    internal_server_error,
    gateway_timeout
)
from src.obtaining import pyDolarVenezuelaApi

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

@app.route('/api/v1/<string:currency>/', methods=["GET"])
def get_monitors(currency: str):
    response = jsonify(api.get_all_monitors(currency=currency))
    return response

@app.route('/api/v1/<string:currency>/page', methods=["GET"])
def get_monitor_by_page_or_monitor(currency: str):
    page    = request.args.get('page', None)
    monitor = request.args.get('monitor', None)

    if not page:
        return jsonify({'error': 'Por favor, proporciona el parametro: (page).'}), 400

    if monitor:
        response = jsonify(api.get_information_monitor(currency, page, monitor))
    else:
        response = jsonify(api.get_specific_page_monitors(page, currency))
    return response

@app.route('/api/v1/<string:currency>/conversion', methods=["GET"])
def value_conversion(currency: str):
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400

    response = jsonify(api.get_price_converted(currency, type, value, monitor))
    return response

@app.route('/api/v1/<string:currency>/unit/<string:key_monitor>', methods=["GET"])
def get_by_monitor(currency: str, key_monitor: str):
    response = jsonify(api.get_information_monitor(currency, monitor_code=key_monitor))
    return response

@app.route('/api/v1/dollar/history')
def get_prices_history():
    response = jsonify(api.get_price_history())
    return response