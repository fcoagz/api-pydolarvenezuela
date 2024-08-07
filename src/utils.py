from datetime import datetime
from typing import List, Dict, Any
from .consts import TIME_ZONE

providers = ['criptodolar', 'bcv', 'italcambio', 'alcambio', 'dolartoday', 'enparalelovzla']

currencies_dict = {
    'dollar': 'usd',
    'euro': 'eur'
}

providers_dict = {
    'Cripto Dolar': 'criptodolar',
    'Banco Central de Venezuela': 'bcv',
    'Italcambio': 'italcambio',
    'Al Cambio': 'alcambio',
    'Dolar Today': 'dolartoday',
    'EnParaleloVzla': 'enparalelovzla'
}

update_schedule = {
    'enparalelovzla': [('08:55', '09:55'), ('12:55', '13:55')],
    'alcambio': [('08:55', '09:55'), ('12:55', '13:55'), ('16:55', '17:55')],
    'bcv': [('16:00', '17:55')]
}

# https://stackoverflow.com/questions/414952/sqlalchemy-datetime-timezone
def format_last_update(results: List[Dict[str, Any]]) -> None:
    """
    Formatea la fecha de la última actualización de los resultados.

    - results: Lista de resultados.
    """
    for result in results:
        if 'last_update' in result:
            last_update = result['last_update']
            last_update_dt = datetime.fromisoformat(last_update)
            last_update_ve = last_update_dt.astimezone(TIME_ZONE)
            
            result.update({'last_update': last_update_ve.strftime('%d/%m/%Y, %I:%M %p')})