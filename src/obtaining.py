from pyDolarVenezuela.pages import BCV, CriptoDolar, ExchangeMonitor, iVenezuela
from pyDolarVenezuela import currency_converter, getdate, pages 
from pyDolarVenezuela import Monitor

provider_dict = {
        "criptodolar": CriptoDolar,
        "bcv": BCV,
        "exchangemonitor": ExchangeMonitor,
        "ivenezuela": iVenezuela
} 

class pyDolarVenezuelaApi:
    def __init__(self) -> None:
        self.monitor = Monitor(CriptoDolar) # DEFAULT

    def get_all_monitors(self, provider: pages.Monitor = CriptoDolar):
        get_monitor = Monitor(provider)
        monitors = get_monitor.get_value_monitors()
        datetime = getdate()

        result = {
            "datetime": datetime,
            "monitors": monitors
        }

        return result
    
    def get_specific_page_monitors(self, page: str):
        try:
            provider = provider_dict[page]

            if provider.name == "Exchange Monitor":
                return {'error': 'Utilice la ruta /exchangemonitor/<monitor>. No podemos ofrecerte todos los monitores en un solo lugar.'}
            else:
                result = self.get_all_monitors(provider)
                return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
        
    def get_information_dollar(self, page: str = None, monitor_code: str = None):
        if not page:
            try:
                result = self.monitor.get_value_monitors(monitor_code)
                return result
            except Exception as e:
                return {'error': f'An error occurred: {str(e)}'}
        else:
            try:
                provider = provider_dict[page]
                
                result = self.get_all_monitors(provider)
                if provider.name == "Exchange Monitor":
                    get_monitor = Monitor(provider)
                    monitor = get_monitor.get_value_monitors(monitor_code)

                    return monitor
                if monitor_code in result['monitors']:
                    return result['monitors'][monitor_code]
                else:
                    return {'error': 'No se encontró el monitor al que quieres acceder'}
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
            monitor = self.get_information_dollar(monitor_code=monitor_code)

            return currency_converter(type, float(value), monitor)
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}