from typing import Dict, Any
from datetime import timedelta
from pyDolarVenezuela import pages, Monitor, Database, CheckVersion, currency_converter, getdate
from pyDolarVenezuela.storage import Cache
from pyDolarVenezuela.models import Page
from .consts import (
    sql_motor,
    sql_host,
    sql_database_name,
    sql_port,
    sql_user,
    sql_password,
    currency_dict,
    provider_dict
)

# Deshabilitar la notificación de la última actualización
CheckVersion.check = False

# Caching
cache = Cache(ttl=timedelta(minutes=5))

class pyDolarVenezuelaApi:
    def get_all_monitors(self, currency: str, provider: Page = pages.CriptoDolar):
        try:
            key = f'{provider.name}:{currency}'
            
            if not cache.get(key):
                monitor = Monitor(provider, currency_dict.get(currency.lower()), db=Database(
                    motor=sql_motor,
                    host=sql_host,
                    database=sql_database_name,
                    port=sql_port,
                    user=sql_user,
                    password=sql_password
                ))
                monitors_dict = {info.pop('key'): info for info in monitor.get_all_monitors()}
                cache.set(key, monitors_dict)
            
            result = {
                "datetime": getdate(),
                "monitors": cache.get(key)
            }
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_specific_page_monitors(self, page: str, currency: str):
        provider = provider_dict.get(page)
        if provider is None:
            return {'error': f'No se encontró el proveedor {page}'}

        return self.get_all_monitors(currency, provider)
    
    def get_information_monitor(self, currency: str, page: str = None, monitor_code: str = None):
        def monitor_squals(monitor_code: str, monitors_founds: Dict[str, Dict[str, Any]]):
            return monitor_code in monitors_founds
        
        if not page:
            result = self.get_all_monitors(currency)

            if not monitor_squals(monitor_code, result['monitors']):
                return {'error': 'No se encontró el monitor al que quieres acceder'}
            return result['monitors'][monitor_code]
        else:
            provider = provider_dict.get(page)
            result = self.get_all_monitors(currency, provider)

            if not monitor_squals(monitor_code, result['monitors']):
                return {'error': 'No se encontró el monitor al que quieres acceder'}
            return result['monitors'][monitor_code]
    
    def get_price_converted(self, currency: str, type: str, value, monitor_code: str):
        try:
            monitor = self.get_information_monitor(currency, monitor_code=monitor_code)
            result = currency_converter(type, float(value), monitor)

            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}