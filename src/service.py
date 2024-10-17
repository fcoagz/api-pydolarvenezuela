import json
from typing import Union, Optional, Literal, Dict, List, Any
from pyDolarVenezuela import getdate, currency_converter
from .data.schemas import HistoryPriceSchema, MonitorSchema
from .cron import monitors
from .core import cache
from .consts import PROVIDERS, CURRENCIES

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

def get_all_monitors(currency: str, provider: str, format_date: Literal['timestamp', 'iso', 'default']) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de un proveedor que estan guardado en caché.

    - currency: Moneda.
    - provider: Proveedor.
    - format_date: Formato de fecha.
    """
    if currency not in CURRENCIES.keys() or provider not in PROVIDERS.values():
        raise ValueError(f'No se encontró {'la moneda' if currency not in CURRENCIES else 'el proveedor'}.')
    
    key = f'{provider}:{CURRENCIES.get(currency)}'
    monitors = json.loads(cache.get(key)) if cache.get(key) else None
    monitors_dict = None
    
    if monitors is not None:
        monitors_serialized = MonitorSchema(custom_format=format_date, many=True).dump(monitors)
        monitors_dict = {data.pop('key'): data for data in monitors_serialized}
    
    result = {
        "datetime": getdate(),
        "monitors": {} if not monitors_dict else monitors_dict
    }
    return result

def get_accurate_monitors(monitor_code: Optional[str], format_date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de las paginas BCV y EnParaleloVzla que estan guardado en caché.

    - monitor_code: Key del monitor.
    - format_date: Formato de fecha.
    """
    default_monitors = ["bcv:usd", "enparalelovzla:usd"]
    monitor_data = {}
    for key in default_monitors:
        data = json.loads(cache.get(key)) if cache.get(key) else None
        
        if data is None:
            continue
        monitors_serialized = MonitorSchema(custom_format=format_date, many=True).dump(data)
        monitors_dict = {data.pop('key'): data for data in monitors_serialized}

        if 'usd' in monitors_dict:
            monitor_data['bcv'] = monitors_dict['usd']
            continue
        monitor_data['enparalelovzla'] = monitors_dict['enparalelovzla']
    
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

def get_page_or_monitor(currency: str, page: Optional[str], monitor_code: Optional[str], format_date: str) -> Union[Dict[str, Any], Dict[str, str]]:    
    """
    Obtiene los monitores de una página o un monitor en específico.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor
    - format_date: Formato de fecha.
    """
    page = 'criptodolar' if page is None else page
    result = get_all_monitors(currency, page, format_date)
    
    if monitor_code:
        result = _get_monitor(monitor_code, result['monitors'])
        if result is None:
            raise KeyError('No se encontró el monitor que estás buscando.')
    return result

def fetch_monitor_data(monitor: Any, monitor_code: str, start_date: str, end_date: str, data_type: Literal['daily', 'history']) -> List[Dict[str, Any]]:
    if data_type == 'history':
        return monitor.get_prices_history(monitor_code, start_date, end_date)
    elif data_type == 'daily':
        return monitor.get_daily_price_monitor(monitor_code, start_date)

def get_monitor_data(currency: str, page: str, monitor_code: str, start_date: str, end_date: str, data_type: Literal['daily', 'history'], format_date: Literal['timestamp', 'iso', 'default']) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de precios de un monitor.
    """
    key = _get_cache_key(page, currency, monitor_code, start_date, end_date, data_type)
    
    if cache.get(key) is None:
        for monitor in monitors:     
            name_page = PROVIDERS.get(monitor.provider.name) 
            currency = CURRENCIES.get(currency, currency)  

            if name_page == page and monitor.currency == currency:
                results = fetch_monitor_data(monitor, monitor_code, start_date, end_date, data_type)  
                
                if not results:
                    raise ValueError('No se encontraron datos para el monitor solicitado.')

                cache.set(key, json.dumps([r.__dict__ for r in results], default=str), ex=1800)
                break
        else:
            raise KeyError('No se encontró el monitor al que quieres acceder.')
    
    data = json.loads(cache.get(key))
    schema = HistoryPriceSchema(custom_format=format_date, many=True).dump(data)
    results = {
        'datetime': getdate(),
        data_type: schema
    }
    return results       

def get_history_prices(currency: str, page: str, monitor_code: str, start_date: str, end_date: str, format_date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene el historial de precios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - start_date: Fecha de inicio.
    - end_date: Fecha de finalización.
    """
    return get_monitor_data(currency, page, monitor_code, start_date, end_date, 'history', format_date)

def get_daily_changes(currency: str, page: str, monitor_code: str, date: str, format_date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los cambios diarios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - date: Fecha.
    """
    return get_monitor_data(currency, page, monitor_code, date, date, 'daily', format_date)

def get_price_converted(currency: str, type: str, value: Union[int, float], page: str, monitor_code: str) -> Union[float, Dict[str, str]]:
    """
    Convierte un valor de una moneda a otra.

    - currency: Moneda.
    - type: Tipo de conversión. (VES, USD, EUR).
    - value: Valor a convertir.
    """
    monitor = get_page_or_monitor(currency, page, monitor_code)
    result = currency_converter(type, float(value), monitor)

    return result