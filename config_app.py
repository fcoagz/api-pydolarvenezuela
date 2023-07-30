from pyDolarVenezuela import Monitor
from util import ranges, categories

monitor = Monitor()

class Api(object):
    def __init__(self) -> None:
        self.categorized_dict: dict = {}
    
    def verify_key(self, key_monitor: str):
        for x, i in enumerate(ranges):
            if key_monitor in i:
                return True
        return False

    def getDollar(self, key_monitor: str):
        print(self.verify_key(key_monitor))
        if not self.verify_key(key_monitor):
            return {'message': f"Monitor with key {key_monitor} not found"}
        return monitor.get_value_monitors(key_monitor, name_property = 'price')
        
    def categorized(self, section_dollar: str, key_monitor: str = None):
        for key, value in monitor.get_value_monitors().items():
            category = 'fecha'
            for i, r in enumerate(ranges):
                if key in r:
                    category = list(categories.keys())[list(categories.values()).index(i)]
                    break
            if category not in self.categorized_dict:
                self.categorized_dict[category] = {}
            self.categorized_dict[category][key] = value

        if section_dollar not in self.categorized_dict:
            return {'message': f'Cannot GET information the parameter: {section_dollar}'}
        if key_monitor != None and key_monitor not in self.categorized_dict[section_dollar]:
            return {'message': f'Cannot GET information the parameter: {key_monitor}'}
        
        return (self.categorized_dict[section_dollar][key_monitor] if key_monitor in self.categorized_dict[section_dollar]
                else self.categorized_dict[section_dollar])