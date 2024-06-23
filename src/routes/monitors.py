from flask import Blueprint, request, jsonify
from ..service import pyDolarVenezuelaApi

route = Blueprint('monitors', __name__)
api   = pyDolarVenezuelaApi()

def handle_response(response):
    """Maneja la respuesta del API."""
    if isinstance(response, dict) and response.get('error'):
        return jsonify(response), 400
    else:
        return jsonify(response), 200

@route.get('/api/v1/<string:currency>')
def get_monitor_by_page_or_monitor(currency: str):
    page    = request.args.get('page', 'criptodolar')
    monitor = request.args.get('monitor', None)

    if monitor:
        response = api.get_information_monitor(currency, page, monitor)
    else:
        response = api.get_specific_page_monitors(page, currency)    
    return handle_response(response)

@route.get('/api/v1/<string:currency>/unit/<string:key_monitor>')
def get_by_monitor(currency: str, key_monitor: str):
    response = api.get_information_monitor(currency, monitor_code=key_monitor)
    return handle_response(response)

@route.get('/api/v1/<string:currency>/conversion')
def value_conversion(currency: str):
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400

    response = api.get_price_converted(currency, type, value, monitor)
    return handle_response(response)