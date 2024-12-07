import json

import requests

from .models import Product

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
}

STOCKS = [356, 16]


def get_metro_products(storeId: int) -> dict:
    """Функция для получения продуктов, с помощью запроса к API METRO."""

    response = requests.post(

        headers=HEADERS,
        url='https://api.metro-cc.ru/products-api/graph',
        data=json.dumps({
            'query': 'query Query { '
                     f'search( storeId: {storeId} ) {{ '
                     'products( '
                     'from: 0 '
                     'size: 100 '
                     'fieldFilters: ['
                     '{ field: "category_id", value: "413939" }'
                     ']) { '
                     'products { '
                     'id name url category_id '
                     'manufacturer { name } '
                     'stocks { prices { old_price price } '
                     '} } } }}'
        }, ensure_ascii=True)
    )
    return response.json()['data']['search']['products']['products']


def refactor_products(products: dict) -> list:
    """Функция для преобразования полученных данных от API METRO в список с продуктами."""

    re_products = [

        Product(
            product['id'],
            product['name'],
            product['url'],
            product['stocks'][0]['prices']['old_price'],
            product['stocks'][0]['prices']['price'],
            product['manufacturer']['name']
        ).as_dict() for product in products if product['stocks'][0]['prices']['old_price'] is not None

    ]

    return re_products


def check_data() -> list:
    """Функция для проверки уже существующих записей в файле с продуктами."""

    try:

        with open('data/products.json', 'r', encoding='UTF-8') as file:
            products = json.loads(file.read())
            return products

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Обработка для случаев, если файл не найден, поврежден или пустой.

        return []


def save_data(products: list) -> None:
    """Функция для сохранения данных в файл с продуктами."""

    with open('data/products.json', 'w', encoding='UTF-8') as file:
        file.write(json.dumps(products, ensure_ascii=False, indent=2))
