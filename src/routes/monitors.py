import re
from typing import Literal
from flask import Blueprint, request, jsonify
from ..decorators import token_required
from ..service import (
    get_page_or_monitor,
    get_accurate_monitors,
    get_price_converted,
    get_history_prices, 
    get_daily_changes as get_daily_changes_
)

route = Blueprint('monitors', __name__)

@route.get('/<string:currency>')
@token_required
def get_monitor_by_page_or_monitor(currency: Literal['dollar', 'euro']):
    try:
        token   = request.headers.get('Authorization')
        page    = request.args.get('page')
        monitor = request.args.get('monitor')

        if token and not page:
            response = get_accurate_monitors(monitor)
        else:
            response = get_page_or_monitor(currency, page, monitor)
            
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@route.get('/<string:currency>/history')
@token_required
def get_history(currency: Literal['dollar', 'euro']):
    try:
        page = request.args.get('page')
        monitor = request.args.get('monitor')
        start_date = request.args.get('start_date')
        end_date   = request.args.get('end_date')

        if not all([page, monitor, start_date, end_date]):
            raise ValueError('Por favor, proporciona los parametros: (page, monitor, start_date y end_date).')
        
        for date in [start_date, end_date]:
            if re.match(r'\d{2}-\d{2}-\d{4}', date) is None:
                raise ValueError('El formato de la fecha debe ser: dd-mm-yyyy.')

        response = get_history_prices(currency, page, monitor, start_date, end_date)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@route.get('/<string:currency>/changes')
@token_required
def get_daily_changes(currency: Literal['dollar', 'euro']):
    try:
        page = request.args.get('page')
        monitor = request.args.get('monitor')
        date = request.args.get('date')

        if not all([page, monitor, date]):
            raise ValueError('Por favor, proporciona los parametros: (page, monitor y date).')
        
        if re.match(r'\d{2}-\d{2}-\d{4}', date) is None:
            raise ValueError('El formato de la fecha debe ser: dd-mm-yyyy.')

        response = get_daily_changes_(currency, page, monitor, date)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@route.get('/<string:currency>/conversion')
@token_required
def value_conversion(currency: Literal['dollar', 'euro']):
    try:
        type    = request.args.get('type', None)
        value   = request.args.get('value', None)
        monitor = request.args.get('monitor', None)

        if not all([type, value, monitor]):
            raise ValueError('Por favor, proporciona los parametros: (type, value y monitor).')
        
        response = get_price_converted(currency, type, value, monitor)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400