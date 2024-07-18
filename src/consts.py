import os
from pyDolarVenezuela.pages import AlCambio, BCV, CriptoDolar, DolarToday, ExchangeMonitor, EnParaleloVzla, Italcambio

sql_motor = os.getenv('SQL_MOTOR')
sql_host = os.getenv('SQL_HOST')
sql_database_name = os.getenv('SQL_DB_NAME')
sql_port = os.getenv('SQL_PORT')
sql_user = os.getenv('SQL_USER')
sql_password = os.getenv('SQL_PASSWORD')

provider_dict = {
    'criptodolar': CriptoDolar,
    'bcv': BCV,
    'exchangemonitor': ExchangeMonitor,
    'italcambio': Italcambio,
    'alcambio': AlCambio,
    'dolartoday': DolarToday,
    'enparalelovzla': EnParaleloVzla
}

currency_dict = {
    'dollar': 'usd',
    'euro': 'eur'
}