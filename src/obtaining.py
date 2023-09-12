from pyDolarVenezuela import Monitor
from src.variables import RANGES, CATEGORIES
from src.tools import get_error

monitor = Monitor()

def check_key(key: str) -> bool:
    return key in RANGES

class Api:
    def __init__(self) -> None:
        self.categorized_dict = {}

    def categorize_monitors(self, section_dollar: str, key_monitor: str = None):
        for key, value in monitor.get_value_monitors().items():

            for category, values in CATEGORIES.items():
                if key in values:
                    break
            else:
                category = 'fecha'

            if category not in self.categorized_dict:
                self.categorized_dict[category] = {}
            self.categorized_dict[category][key] = value

        if section_dollar not in self.categorized_dict:
            return get_error("section_dollar", section_dollar)
        if key_monitor is not None and key_monitor not in self.categorized_dict[section_dollar]:
            return get_error("key_monitor", key_monitor)
        
        return (self.categorized_dict[section_dollar][key_monitor] if key_monitor in self.categorized_dict[section_dollar]
                else self.categorized_dict[section_dollar])
    
    def get_all_monitors(self):
        monitors = monitor.get_value_monitors()
        result = {
            "datetime": monitors.pop("datetime"),
            "monitors": monitors
        }
        return result
    
    def get_dollar(self, key_monitor: str):
        if not check_key(key_monitor):
            return get_error("key_monitor", key_monitor)
        try:
            result = monitor.get_value_monitors(key_monitor, name_property='price')
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        
    def get_monitor(self, key_monitor: str):
        if not check_key(key_monitor):
            return get_error("key_monitor", key_monitor)
        try:
            result = monitor.get_value_monitors(key_monitor)
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        