from typing import Literal
from flask import Blueprint, request, jsonify
from ..decorators import token_required_user, token_optional_user
from ..service import (
    get_page_or_monitor,
    get_accurate_monitors,
    get_price_converted,
    get_history_prices, 
    get_daily_changes as get_daily_changes_
)

route = Blueprint('monitors', __name__)

def handle_response(response):
    """Maneja la respuesta del API."""
    if isinstance(response, dict) and response.get('error'):
        return jsonify(response), 400
    else:
        return jsonify(response), 200

@route.get('/api/v1/<string:currency>')
@token_optional_user
def get_monitor_by_page_or_monitor(currency: Literal['dollar', 'euro']):
    token   = request.headers.get('Authorization')
    page    = request.args.get('page')
    monitor = request.args.get('monitor')

    if token:
        if not page:
            response = get_accurate_monitors(monitor)
        else:
            response = get_page_or_monitor(currency, page, monitor)
    else:
        response = get_page_or_monitor(currency, page, monitor)
        
    return handle_response(response)

@route.get('/api/v1/<string:currency>/history')
@token_required_user
def get_history(currency: Literal['dollar', 'euro']):
    page   = request.args.get('page')
    monitor = request.args.get('monitor')
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    response = get_history_prices(currency, page, monitor, start_date, end_date)
    return handle_response(response)

@route.get('/api/v1/<string:currency>/changes')
@token_required_user
def get_daily_changes(currency: Literal['dollar', 'euro']):
    page = request.args.get('page')
    monitor = request.args.get('monitor')
    date = request.args.get('date')

    response = get_daily_changes_(currency, page, monitor, date)
    return handle_response(response)

@route.get('/api/v1/<string:currency>/conversion')
@token_optional_user
def value_conversion(currency: Literal['dollar', 'euro']):
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400
    
    response = get_price_converted(currency, type, value, monitor)
    return handle_response(response)