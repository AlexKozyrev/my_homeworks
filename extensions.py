import json

import requests

keys = {
    'рубль': 'RUB',
    'евро': 'EUR',
    'доллар': 'USD'
}


class APIException(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        try:
            quote_f = keys[quote]  # получаем код валюты
        except KeyError:
            raise APIException(f'Ошибка в получении цены: неизвестная валюта {quote}')
        try:
            base_f = keys[base]  # получаем код валюты
        except KeyError:
            raise APIException(f'Ошибка в получении цены: неизвестная валюта {base}')
        response = requests.get(
            f'https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_j7dXZxUeOw1LdLc3syWBb4JJL8NxbpQ0GBWFLxkt&currencies={quote_f}&base_currency={base_f}')
        if response.status_code != 200:
            raise APIException(f'Error in get_price: {response.status_code}')
        try:
            data = json.loads(response.content.decode('utf-8'))
            rate = data['data'][quote_f]  # получаем курс первой валюты ко второй
        except KeyError:
            raise APIException(f'Ошибка в получении цены: неизвестная валюта {quote_f}')
        return rate * amount  # получаем итоговую сумму валюты
