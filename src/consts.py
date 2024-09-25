import os
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()

SQL_MOTOR      = os.getenv('SQL_MOTOR')
SQL_HOST       = os.getenv('SQL_HOST')
SQL_DB_NAME    = os.getenv('SQL_DB_NAME')
SQL_PORT       = os.getenv('SQL_PORT')
SQL_USER       = os.getenv('SQL_USER')
SQL_PASSWORD   = os.getenv('SQL_PASSWORD')

REDIS_HOST     = os.getenv('REDIS_HOST')
REDIS_PORT     = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
REDIS_DB       = os.getenv('REDIS_DB', 0) # default 0

TOKEN_SECRET   = os.getenv('TOKEN_SECRET')
TIMEOUT        = int(os.getenv('TIMEOUT', 15)) # in minutes

TIME_ZONE      = os.getenv('TIMEZONE', 'America/Caracas')
TIME_ZONE      = timezone(TIME_ZONE)

PROVIDERS = {
    'Al Cambio': 'alcambio',
    'Banco Central de Venezuela': 'bcv',
    'Cripto Dolar': 'criptodolar',
    'Dolar Today': 'dolartoday',
    'EnParaleloVzla': 'enparalelovzla',
    'Italcambio': 'italcambio'
}
CURRENCIES = {
    'dollar': 'usd',
    'euro': 'eur'
}
UPDATE_SCHEDULE = {
    'enparalelovzla': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('08:55', '09:55'),
            ('12:55', '13:55')
        ]
    },
    'alcambio': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('08:55', '09:55'),
            ('12:55', '13:55'),
            ('16:55', '17:55')
        ]
    },
    'bcv': {
        'not': [
            'Sat', 'Sun'
        ], 'hours': [
            ('16:00', '17:55')
        ]
    }
}

if os.getenv('GETLOGS') == 'True':
    GETLOGS = True
else:
    GETLOGS = False

URL_DB  = f'{SQL_MOTOR}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}'