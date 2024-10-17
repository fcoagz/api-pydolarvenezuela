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
from .consts import (
    SQL_HOST,
    SQL_MOTOR,
    SQL_DB_NAME,
    SQL_PORT,
    SQL_USER,
    SQL_PASSWORD,
    TIME_ZONE,
    CURRENCIES,
    PROVIDERS,
    UPDATE_SCHEDULE
)

CheckVersion.check = False

pages    = [AlCambio, BCV, CriptoDolar, DolarToday, EnParaleloVzla, Italcambio]
monitors = [Monitor(page, currency, db=Database(
    SQL_MOTOR, SQL_HOST, SQL_DB_NAME, SQL_PORT, SQL_USER, SQL_PASSWORD
    )) for currency in CURRENCIES.values() for page in pages if currency in page.currencies]

def update_data(name: str, monitor: Monitor) -> None:
    """
    Obtiene los datos de un monitor y los guarda en caché.

    - name: Nombre del proveedor.
    - monitor: Instancia de Monitor.
    """
    try:
        cache.set(f'{name}:{monitor.currency}', json.dumps(
            [m.__dict__ for m in monitor.get_all_monitors()], default=str))
    except Exception as e:
        logger.warning(f'Error al obtener datos de {monitor.provider.name}: {str(e)}')

def reload_monitors() -> None:
    """
    Recarga los datos de los monitores y los guarda en caché.
    """
    for monitor in monitors:
        name = PROVIDERS.get(monitor.provider.name)
        logger.info(f'Recargando datos de "{monitor.provider.name}".')
        update_data(name, monitor)

def job() -> None:
    """
    Itera sobre los monitores y actualiza los datos en caché.\n
    Actualiza los datos de un monitor si la hora actual está dentro del rango de actualización.
    """
    dt   = datetime.now(TIME_ZONE)
    _day_  = dt.strftime('%a')
    _hour_ = dt.strftime('%H:%M')

    for monitor in monitors:
        name = PROVIDERS.get(monitor.provider.name)
        
        if name not in UPDATE_SCHEDULE.keys():
            logger.info(f'Actualizando datos de "{monitor.provider.name}".')
            update_data(name, monitor)
            continue

        if _day_ in UPDATE_SCHEDULE.get(name, {}).get('not', []):
            continue

        for start, end in UPDATE_SCHEDULE.get(name, {}).get('hours', []):
            if _hour_ >= start and _hour_ <= end:
                logger.info(f'Actualizando datos de "{monitor.provider.name}".')
                update_data(name, monitor)
                break