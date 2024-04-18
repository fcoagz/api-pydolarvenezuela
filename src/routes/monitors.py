from flask import Blueprint, request, jsonify
from ..utils.pydolarvenezuela import pyDolarVenezuelaApi
from ..utils.cache import cache

route = Blueprint('monitors', __name__)
api   = pyDolarVenezuelaApi()

@route.get('/api/v1/<string:currency>')
def get_monitor_by_page_or_monitor(currency: str):
    page    = request.args.get('page', 'criptodolar')
    monitor = request.args.get('monitor', None)
    key     = f'{currency}:{page}:{monitor}'
    
    if not cache.get_data(key):
        if monitor:
            response = jsonify(api.get_information_monitor(currency, page, monitor)), 200
            cache.set_data(key, response)
        else:
            response = jsonify(api.get_specific_page_monitors(page, currency)), 200
            cache.set_data(key, response)
    return cache.get_data(key)

@route.get('/api/v1/<string:currency>/unit/<string:key_monitor>')
def get_by_monitor(currency: str, key_monitor: str):
    key = f'{currency}:unit:{key_monitor}'

    if not cache.get_data(key):
        response = jsonify(api.get_information_monitor(currency, monitor_code=key_monitor)), 200
        cache.set_data(key, response)
    return cache.get_data(key)

@route.get('/api/v1/<string:currency>/conversion')
def value_conversion(currency: str):
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400

    response = jsonify(api.get_price_converted(currency, type, value, monitor)), 200
    return response