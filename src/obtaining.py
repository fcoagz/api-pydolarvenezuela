from pyDolarVenezuela import Monitor
from src.variables import ranges, categories
monitor = Monitor()

def check_key(key: str) -> bool:
    for x, i in enumerate(ranges):
        if key in i:
            return True
    return False

class Api:
    def __init__(self) -> None:
        self.categorized_dict = {}

    def categorize_monitors(self, section_dollar: str, key_monitor: str = None):
        for key, value in monitor.get_value_monitors().items():
            category = 'fecha'
            for i, values in enumerate(ranges):
                if key in values:
                    category = list(categories.keys())[list(categories.values()).index(i)]
                    break
            if category not in self.categorized_dict:
                self.categorized_dict[category] = {}
            self.categorized_dict[category][key] = value

        if section_dollar not in self.categorized_dict:
            return {'error': f'Invalid section_dollar: {section_dollar}'}
        if key_monitor is not None and key_monitor not in self.categorized_dict[section_dollar]:
            return {'error': f'Invalid key_monitor: {key_monitor}'}
        
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
            return {'error': f'Invalid key_monitor: {key_monitor}'}
        try:
            result = monitor.get_value_monitors(key_monitor, name_property='price')
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        
    def get_monitor(self, key_monitor: str):
        if not check_key(key_monitor):
            return {'error': f'Invalid key_monitor: {key_monitor}'}
        try:
            result = monitor.get_value_monitors(key_monitor)
            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        