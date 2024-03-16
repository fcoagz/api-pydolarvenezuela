from flask import Blueprint, request, jsonify
from ..utils.pydolarvenezuela import pyDolarVenezuelaApi

route = Blueprint('monitors', __name__)
api   = pyDolarVenezuelaApi()

@route.get('/api/v1/<string:currency>')
def get_monitor_by_page_or_monitor(currency: str):
    page    = request.args.get('page', None)
    monitor = request.args.get('monitor', None)

    if not page:
        page = 'criptodolar'
    if monitor:
        response = jsonify(api.get_information_monitor(currency, page, monitor)), 200
    else:
        response = jsonify(api.get_specific_page_monitors(page, currency)), 200
    return response

@route.get('/api/v1/<string:currency>/unit/<string:key_monitor>')
def get_by_monitor(currency: str, key_monitor: str):
    response = jsonify(api.get_information_monitor(currency, monitor_code=key_monitor)), 200
    return response

@route.get('/api/v1/<string:currency>/conversion')
def value_conversion(currency: str):
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400

    response = jsonify(api.get_price_converted(currency, type, value, monitor)), 200
    return response