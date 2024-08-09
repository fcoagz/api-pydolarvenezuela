import json
from datetime import datetime
from pyDolarVenezuela.pages import (
    AlCambio, 
    BCV, 
    CriptoDolar, 
    DolarToday, 
    EnParaleloVzla, 
    Italcambio
)
from pyDolarVenezuela import Monitor, Database, CheckVersion
from .core import logger
from .core import cache
from .utils import currencies_dict, providers_dict, update_schedule, format_last_update
from .consts import (
    SQL_HOST,
    SQL_MOTOR,
    SQL_DB_NAME,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    TIME_ZONE
)

CheckVersion.check = False

pages    = [AlCambio, BCV, CriptoDolar, DolarToday, EnParaleloVzla, Italcambio]
monitors = [Monitor(page, currency, db=Database(
    SQL_MOTOR, SQL_HOST, SQL_DB_NAME, SQL_PORT, SQL_USER, SQL_PASSWORD
    )) for currency in currencies_dict.values() for page in pages if currency in page.currencies]

def update_data(name: str, monitor: Monitor) -> None:
    """
    Obtiene los datos de un monitor y los guarda en caché.

    - name: Nombre del proveedor.
    - monitor: Instancia de Monitor.
    """
    try:
        monitors = format_last_update(monitor.get_all_monitors())
        monitors_dict = {data.__dict__.pop('key'): data.__dict__ for data in monitors}
        cache.set(f'{name}:{monitor.currency}', json.dumps(monitors_dict))
    except Exception as e:
        logger.warning(f'Error al obtener datos de {monitor.provider.name}: {str(e)}')

def reload_monitors() -> None:
    """
    Recarga los datos de los monitores y los guarda en caché.
    """
    for monitor in monitors:
        name = providers_dict.get(monitor.provider.name)
        logger.info(f'Recargando datos de "{monitor.provider.name}".')
        update_data(name, monitor)

def job() -> None:
    """
    Itera sobre los monitores y actualiza los datos en caché.\n
    Actualiza los datos de un monitor si la hora actual está dentro del rango de actualización.
    """
    hour_current = datetime.now(TIME_ZONE).strftime('%H:%M')
    for monitor in monitors:
        name = providers_dict.get(monitor.provider.name)
        
        if name not in update_schedule:
            logger.info(f'Actualizando datos de "{monitor.provider.name}".')
            update_data(name, monitor)
            continue
        
        for start, end in update_schedule.get(name, []):
            if hour_current >= start and hour_current <= end:
                logger.info(f'Actualizando datos de "{monitor.provider.name}".')
                update_data(name, monitor)
                break