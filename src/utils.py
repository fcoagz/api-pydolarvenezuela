from pyDolarVenezuela.models import Monitor, HistoryPrice
from typing import List, Union
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
def format_last_update(results: List[Union[Monitor, HistoryPrice]]) -> List[Union[Monitor, HistoryPrice]]:
    """
    Formatea la fecha de la última actualización de los resultados.

    - results: Lista de resultados.
    """
    for result in results:
        last_update_obj = result.last_update.astimezone(TIME_ZONE)
        result.last_update = last_update_obj.strftime('%d/%m/%Y, %I:%M %p')
    return results