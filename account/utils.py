import requests
from django.conf import settings


def register_order(amount):
    data = {
        'userName': settings.SBER_LOGIN,
        'password': settings.SBER_PASSWORD,
        'amount': amount,
        'currency': 'RUB',
        'returnUrl': 'https://www.google.com',
        'failUrl': 'https://yandex.ru'
    }
    r = requests.post('https://3dsec.sberbank.ru/payment/rest/register.do/', data)
    print(r)
    return r
