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