import json
from typing import Union, Optional, Dict, List, Any
from pyDolarVenezuela import getdate, currency_converter
from .cron import monitors
from .core import cache
from .consts import TIME_ZONE
from .utils import providers, providers_dict, currencies_dict

def format_prices_history(results: List[Dict[str, Any]]) -> None:
    """
    Formatea las fechas de un historial de monitor.

    - results: Lista de resultados.
    """
    for result in results:
        if 'last_update' in result:
            last_update = result['last_update']
            last_update_ve = last_update.astimezone(TIME_ZONE)
            formatted_last_update = last_update_ve.strftime('%d/%m/%Y, %I:%M %p')
            result.update({'last_update': formatted_last_update})

def _get_monitor(monitor_code: str, monitors_founds: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Obtiene un monitor en específico.

    - monitor_code: Key del monitor.
    - monitors_founds: Monitores encontrados.
    """
    if monitor_code in monitors_founds:
        return monitors_founds[monitor_code]
    return {'error': 'No se encontró el monitor al que quieres acceder'}

def get_all_monitors(currency: str, provider: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de un proveedor que estan guardado en caché.

    - currency: Moneda.
    - provider: Proveedor.
    """
    try:
        if currency not in currencies_dict:
            return {'error': f'No se encontró la moneda {currency}'}
        if provider not in providers:
            return {'error': f'No se encontró el proveedor {provider}'}
        
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
    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}

def get_accurate_monitors(monitor_code: Optional[str] = None) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los monitores de las paginas BCV y EnParaleloVzla que estan guardado en caché.

    - monitor_code: Key del monitor.
    """
    default_monitors = ["bcv:usd", "enparalelovzla:usd"]
    try:
        monitor_data = {}
        for key in default_monitors:
            data = cache.get(key)
            
            if data is None:
                continue
            data = json.loads(data)

            if 'usd' in data:
                monitor_data['bcv'] = data['usd']
            monitor_data['enparalelovzla'] = data['enparalelovzla']
        
        result = {
            "datetime": getdate(),
            "monitors": monitor_data
        }

        if monitor_code:
            return _get_monitor(monitor_code, result['monitors'])
        return result
    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}

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

def get_history_monitor(currency: str, page: str, monitor_code: str, start_date: str, end_date: str) -> List[Dict[str, Any]]:
    """
    Obtiene el historial de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - start_date: Fecha de inicio.
    - end_date: Fecha de fin.
    """
    try:
        key = f'{page}:{currency}:{monitor_code}:{start_date}:{end_date}' 
        
        if cache.get(key) is None:
            for monitor in monitors:     
                name_page = providers_dict.get(monitor.provider.name) 
                currency = currencies_dict.get(currency, currency)  

                if name_page == page and monitor.currency == currency:
                    results = monitor.get_prices_history(monitor_code, start_date, end_date)  
                    
                    if not results:
                        return {'error': 'No se encontró historial de precios.'}
                    
                    format_prices_history(results)
                    results = {
                        'datetime': getdate(),
                        'history': results}
                    
                    cache.set(key, json.dumps(results), ex=1800)
                    break
            else:
                return {'error': 'No se encontró el monitor al que quieres acceder.'}
        results = json.loads(cache.get(key))
        return results       
    except Exception as e:
        return {'error': f'Ocurrió un error: {str(e)}'}

def get_daily_changes(currency: str, page: str, monitor_code: str, date: str) -> Union[Dict[str, Any], Dict[str, str]]:
    """
    Obtiene los cambios diarios de un monitor.

    - currency: Moneda.
    - page: Página.
    - monitor_code: Key del monitor.
    - date: Fecha.
    """
    try:
        key = f'{page}:{currency}:{monitor_code}:{date}'
        
        if cache.get(key) is None:
            for monitor in monitors:
                name_page = providers_dict.get(monitor.provider.name)
                currency = currencies_dict.get(currency, currency)

                if name_page == page and monitor.currency == currency:
                    results = monitor.get_daily_price_monitor(monitor_code, date)
                    
                    if not results:
                        return {'error': 'No se encontraron cambios diarios.'}
                    
                    format_prices_history(results)
                    results = {
                        'datetime': getdate(),
                        'changes': results}

                    cache.set(key, json.dumps(results), ex=1800)
                    break
            else:
                return {'error': 'No se encontró el monitor al que quieres acceder.'}
        results = json.loads(cache.get(key))
        return results
    except Exception as e:
        return {'error': f'Ocurrió un error: {str(e)}'}

def get_price_converted(currency: str, type: str, value, monitor_code: str) -> Union[float, Dict[str, str]]:
    """
    Convierte un valor de una moneda a otra.

    - currency: Moneda.
    - type: Tipo de conversión. (VES, USD, EUR).
    - value: Valor a convertir.
    """
    try:
        monitor = get_page_or_monitor(currency, monitor_code=monitor_code)
        result = currency_converter(type, float(value), monitor)

        return result
    except Exception as e:
        return {'error': f'An error occurred: {str(e)}'}