from pyDolarVenezuela.pages import BCV, CriptoDolar, ExchangeMonitor, iVenezuela, Dpedidos
from pyDolarVenezuela.pages import Monitor as Page
from pyDolarVenezuela import Monitor, currency_converter, getdate

class pyDolarVenezuelaApi:
    def __init__(self) -> None:
        self.provider_dict = {
            "criptodolar": CriptoDolar,
            "bcv": BCV,
            "exchangemonitor": ExchangeMonitor,
            "ivenezuela": iVenezuela,
            "dpedidos": Dpedidos
        }
        self.currency_dict = {
            "dollar": "usd",
            "euro": "eur"
        }
    
    def get_all_monitors(self, currency: str, provider: Page = CriptoDolar):
        monitor = Monitor(provider=provider, currency=self.currency_dict.get(currency))
        monitors = monitor.get_value_monitors()
        datetime = getdate()

        result = {
            "datetime": datetime,
            "monitors": monitors
        }

        return result
    
    def get_specific_page_monitors(self, page: str, currency: str):
        try:
            provider = self.provider_dict.get(page)
            result = self.get_all_monitors(currency, provider)

            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    def get_information_monitor(self, currency: str, page: str = None, monitor_code: str = None):
        if not page:
            try:
                monitor = self.get_all_monitors(currency)
                result = monitor['monitors'][monitor_code]

                return result
            except Exception as e:
                return {'error': f'An error occurred: {str(e)}'}
        else:
            try:
                provider = self.provider_dict.get(page)
                result = self.get_all_monitors(currency, provider)

                if monitor_code in result['monitors']:
                    return result['monitors'][monitor_code]
                else:
                    return {'error': 'No se encontró el monitor al que quieres acceder'}
            except Exception as e:
                return {'error': f'An error occurred: {str(e)}'}
    
    def get_price_converted(self, currency: str, type: str, value, monitor_code: str):
        try:
            monitor = self.get_information_monitor(currency, monitor_code=monitor_code)
            result = currency_converter(type, float(value), monitor)

            return result
        except Exception as e:
            return {'error': f'An error occurred: {str(e)}'}
    
    # def get_price_history(self):
    #     storage = 'https://storage-pydolarvenezuela.vercel.app/dolarhistorial'
    #     headers = {'SECRET_KEY': os.getenv('SECRET_KEY')}

    #     try:
    #         response = requests.get(storage, headers=headers)
    #         response.raise_for_status()

    #         return response.json()
    #     except Exception as e:
    #         return {'error': f'An error occurred: {str(e)}'}