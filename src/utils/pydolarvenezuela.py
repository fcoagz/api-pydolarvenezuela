import os
from pyDolarVenezuela.pages import AlCambio, BCV, CriptoDolar, ExchangeMonitor, Italcambio
from pyDolarVenezuela.pages import Page
from pyDolarVenezuela import Monitor, Redis, CheckVersion, currency_converter, getdate
from .cache import Cache

CheckVersion.check = False

redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')
redis_password = os.getenv('REDIS_PASSWORD')

cache = Cache(maxsize=1024, timeout=300)
db = Redis(
  host=redis_host,
  port=redis_port,
  password=redis_password
)

class pyDolarVenezuelaApi:    
    provider_dict = {
        "criptodolar": CriptoDolar,
        "bcv": BCV,
        "exchangemonitor": ExchangeMonitor,
        "italcambio": Italcambio,
        "alcambio": AlCambio
    }

    currency_dict = {
        "dollar": "usd",
        "euro": "eur"
    }

    def get_all_monitors(self, currency: str, provider: Page = CriptoDolar):
        try:
            key = f'{currency}:{provider.name}'

            if not cache.get_data(key):
                monitor = Monitor(provider=provider, currency=self.currency_dict.get(currency), db=db)
                monitors = monitor.get_value_monitors()

                cache.set_data(key, monitors)
            
            result = {
                "datetime": getdate(),
                "monitors": cache.get_data(key)
            }
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_specific_page_monitors(self, page: str, currency: str):
        try:
            provider = self.provider_dict.get(page)
            if provider is None:
                return {'error': f'No se encontró el proveedor {page}'}

            return self.get_all_monitors(currency, provider)
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_information_monitor(self, currency: str, page: str = None, monitor_code: str = None):
        if not page:
            try:
                monitor = self.get_all_monitors(currency)
                result = monitor['monitors'][monitor_code]

                return result
            except Exception as e:
                return {'error': f'An error occurred: {str(e)}'}
        else:
            try:
                provider = self.provider_dict.get(page)
                result = self.get_all_monitors(currency, provider)

                if monitor_code not in result['monitors']:
                    return {'error': 'No se encontró el monitor al que quieres acceder'}

                return result['monitors'][monitor_code]
            except Exception as e:
                return {'error': f'An error occurred: {str(e)}'}
    
    def get_price_converted(self, currency: str, type: str, value, monitor_code: str):
        try:
            monitor = self.get_information_monitor(currency, monitor_code=monitor_code)
            result = currency_converter(type, float(value), monitor)

            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}