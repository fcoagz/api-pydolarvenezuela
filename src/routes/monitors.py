from typing import Literal
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from ..data.engine import engine
from ..data.services import is_user_valid
from ..core import limiter
from ..service import (
    get_page_or_monitor,
    get_accurate_monitors,
    get_price_converted,
    get_history_prices, 
    get_daily_changes as get_daily_changes_
)

route   = Blueprint('monitors', __name__)
session = sessionmaker(bind=engine)()

def handle_response(response):
    """Maneja la respuesta del API."""
    if isinstance(response, dict) and response.get('error'):
        return jsonify(response), 400
    else:
        return jsonify(response), 200

@route.get('/api/v1/<string:currency>')
def get_monitor_by_page_or_monitor(currency: Literal['dollar', 'euro']):
    token   = request.headers.get('Authorization')
    page    = request.args.get('page')
    monitor = request.args.get('monitor')

    if token:
        if not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401
        
        if not page:
            response = get_accurate_monitors(monitor)
            return handle_response(response)
        else:
            response = get_page_or_monitor(currency, page, monitor)
            return handle_response(response)
    
    limiter.limit("100 per hour")(lambda: None)()
    response = get_page_or_monitor(currency, page, monitor)
    return handle_response(response)
    
# @route.get('/api/v1/<string:currency>/unit/<string:key_monitor>')
# def get_by_monitor(currency: Literal['dollar', 'euro'], key_monitor: str):
#     response = get_page_or_monitor(currency, monitor_code=key_monitor)
#     return handle_response(response)

@route.get('/api/v1/<string:currency>/history')
def get_history(currency: Literal['dollar', 'euro']):
    token   = request.headers.get('Authorization')
    page   = request.args.get('page')
    monitor = request.args.get('monitor')
    start_date = request.args.get('start_date')
    end_date   = request.args.get('end_date')

    if token:
        if not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401
        
        response = get_history_prices(currency, page, monitor, start_date, end_date)
        return handle_response(response)
    else:
        return jsonify({'error': 'Requiere token para acceder'}), 401

@route.get('/api/v1/<string:currency>/changes')
def get_daily_changes(currency: Literal['dollar', 'euro']):
    token = request.headers.get('Authorization')
    page = request.args.get('page')
    monitor = request.args.get('monitor')
    date = request.args.get('date')

    if token:
        if not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401

        response = get_daily_changes_(currency, page, monitor, date)
        return handle_response(response)
    else:
        return jsonify({'error': 'Requiere token para acceder'}), 401

@route.get('/api/v1/<string:currency>/conversion')
def value_conversion(currency: Literal['dollar', 'euro']):
    token   = request.headers.get('Authorization')
    type    = request.args.get('type', None)
    value   = request.args.get('value', None)
    monitor = request.args.get('monitor', None)

    if not type or not value or not monitor:
        return jsonify({'error': 'Por favor, proporciona los parametros: (type, value y monitor).'}), 400
    
    if token:
        if not is_user_valid(session, token):
            return jsonify({'error': 'Token no válido.'}), 401
        
        response = get_price_converted(currency, type, value, monitor)
        return handle_response(response)

    limiter.limit("100 per hour")(lambda: None)()
    response = get_price_converted(currency, type, value, monitor)
    return handle_response(response)