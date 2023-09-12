from src.tools import functools_reduce_iconcat


CATEGORIES = {
    'dolar_promedio': ['dolar_em', 'monitor_dolar_venezuela', 'enparalelovzla', 'monitor_dolar_vzla'],
    'bcv_oficial': ['petro', 'bcv', 'remesas_zoom', 'italcambio', 'bancamiga', 'banco_de_venezuela', 'banco_exterior', 'banplus', 'bnc', 'banesco', 'bbva_provincial', 'mercantil', 'otras_instituciones'],
    'paginas': ['binance', 'airtm', 'reserve', 'syklo', 'yadio', 'dolartoday', 'dolartoday_(btc)', 'mkambio', 'cambios_r&a'],
    'monederos_electronicos': ['paypal', 'zinli', 'skrill', 'amazon_gift_card']
}

RANGES = functools_reduce_iconcat(CATEGORIES.values())