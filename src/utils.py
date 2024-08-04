from typing import List, Dict, Any

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

def format_last_update(results: List[Dict[str, Any]]) -> None:
    """
    Formatea la fecha de la última actualización de los resultados.

    - results: Lista de resultados.
    """
    for result in results:
        if 'last_update' in result:
            last_update = result['last_update']
            formatted_last_update = last_update.strftime('%d/%m/%Y, %I:%M %p')
            result.update({'last_update': formatted_last_update})