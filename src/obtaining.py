from pyDolarVenezuela.pages import CriptoDolar
from pyDolarVenezuela.tools import TimeDollar
from pyDolarVenezuela import Monitor, currency_converter

# from src.variables import RANGES, CATEGORIES
# from src.tools import get_error

# def check_key(key: str) -> bool:
#     return key in RANGES

class NewApi:
    def __init__(self, Provider=CriptoDolar) -> None:
        self.monitor = Monitor(Provider)
        self.time    = TimeDollar()
    
    def get_all_monitors(self):
        monitors = self.monitor.get_value_monitors()
        datetime = self.time.get_time_zone()

        result = {
            "datetime": datetime,
            "monitors": monitors
        }

        return result
    
    def get_information_dollar(self, monitor_code: str):
        try:
            result = self.monitor.get_value_monitors(monitor_code)
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_price_dollar(self, monitor_code: str):
        try:
            result = self.monitor.get_value_monitors(monitor_code, name_property='price')
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_price_converted(self, type: str, value, monitor_code: dict):
        try:
            monitor = self.get_information_dollar(monitor_code)

            return currency_converter(type, value, monitor)
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        