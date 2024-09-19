import json
from typing import Union, Optional, Literal, Dict, List, Any
from pyDolarVenezuela import getdate, currency_converter
from .data.schemas import HistoryPriceSchema
from .cron import monitors
from .core import cache
from .utils import providers, providers_dict, currencies_dict

history_price_schema = HistoryPriceSchema()

def _get_cache_key(*args) -> str:
    """
    Obtiene la clave de caché.
    """
    return ':'.join(args)

def _get_monitor(monitor_code: str, monitors_founds: Dict[str, Dict[str, Any]]) -> Union[Dict[str, Any], None]:
    """
    Obtiene un monitor en específico.

    - monitor_code: Key del monitor.
    - monitors_founds: Monitores encontrados.
    """
    if monitor_code in monitors_founds:
        return monitors_founds[monitor_code]
    return None

def get_all_monitors(currency: str, provider: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de un proveedor que estan guardado en caché.

    - currency: Moneda.
    - provider: Proveedor.
    """
    if currency not in currencies_dict or provider not in providers:
        raise ValueError(f'No se encontró {'la moneda' if currency not in currencies_dict else 'el proveedor'}.')
    
    key = f'{provider}:{currencies_dict.get(currency)}'
    monitors = cache.get(key)
    monitors_dict = {}
    
    if monitors is not None:
        monitors_dict = json.loads(monitors)
    
    result = {
        "datetime": getdate(),
        "monitors": monitors_dict
    }
    return result

def get_accurate_monitors(monitor_code: Optional[str] = None) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de las paginas BCV y EnParaleloVzla que estan guardado en caché.

    - monitor_code: Key del monitor.
    """
    default_monitors = ["bcv:usd", "enparalelovzla:usd"]
    monitor_data = {}
    for key in default_monitors:
        data = cache.get(key)
        
        if data is None:
            continue
        data = json.loads(data)

        if 'usd' in data:
            monitor_data['bcv'] = data['usd']
            continue
        monitor_data['enparalelovzla'] = data['enparalelovzla']
    
    if monitor_code:
        result = _get_monitor(monitor_code, monitor_data)
        if result is None:
            raise KeyError('No se encontró el monitor que estás buscando.')
        return result
    
    result = {
        "datetime": getdate(),
        "monitors": monitor_data
    }
    return result

def get_page_or_monitor(currency: str, page: Optional[str] = None, monitor_code: Optional[str] = None) -> Union[Dict[str, Any], Dict[str, str]]:    
    """
    Obtiene los monitores de una página o un monitor en específico.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor
    """
    page = 'criptodolar' if page is None else page
    result = get_all_monitors(currency, page)
    
    if monitor_code:
        return _get_monitor(monitor_code, result['monitors'])
    return result

def fetch_monitor_data(monitor: Any, monitor_code: str, start_date: str, end_date: str, data_type: Literal['daily', 'history']) -> List[Dict[str, Any]]:
    if data_type == 'history':
        return monitor.get_prices_history(monitor_code, start_date, end_date)
    elif data_type == 'daily':
        return monitor.get_daily_price_monitor(monitor_code, start_date)

def get_monitor_data(currency: str, page: str, monitor_code: str, start_date: str, end_date: str, data_type: Literal['daily', 'history']) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de precios de un monitor.
    """
    key = _get_cache_key(page, currency, monitor_code, start_date, end_date, data_type)
    
    if cache.get(key) is None:
        for monitor in monitors:     
            name_page = providers_dict.get(monitor.provider.name) 
            currency = currencies_dict.get(currency, currency)  

            if name_page == page and monitor.currency == currency:
                results = fetch_monitor_data(monitor, monitor_code, start_date, end_date, data_type)  
                
                if not results:
                    raise ValueError('No se encontraron datos para el monitor solicitado.')
                
                results_dict = history_price_schema.dump(results, many=True)
                cache.set(key, json.dumps(results_dict), ex=1800)
                break
        else:
            raise KeyError('No se encontró el monitor al que quieres acceder.')
    
    data = json.loads(cache.get(key))
    results = {
        'datetime': getdate(),
        data_type: data
    }
    return results       

def get_history_prices(currency: str, page: str, monitor_code: str, start_date: str, end_date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene el historial de precios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - start_date: Fecha de inicio.
    - end_date: Fecha de finalización.
    """
    return get_monitor_data(currency, page, monitor_code, start_date, end_date, 'history')

def get_daily_changes(currency: str, page: str, monitor_code: str, date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los cambios diarios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - date: Fecha.
    """
    return get_monitor_data(currency, page, monitor_code, date, date, 'daily')

def get_price_converted(currency: str, type: str, value, monitor_code: str) -> Union[float, Dict[str, str]]:
    """
    Convierte un valor de una moneda a otra.

    - currency: Moneda.
    - type: Tipo de conversión. (VES, USD, EUR).
    - value: Valor a convertir.
    """
    monitor = get_page_or_monitor(currency, monitor_code=monitor_code)
    result = currency_converter(type, float(value), monitor)

    return result