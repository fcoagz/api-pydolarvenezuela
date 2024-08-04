import os
import pytz
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

if os.getenv('GETLOGS') == 'True':
    GETLOGS = True
else:
    GETLOGS = False

URL_DB  = f'{SQL_MOTOR}://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DB_NAME}'
# URL_REDIS = f'redis://{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

TIME_ZONE = pytz.timezone('America/Caracas')