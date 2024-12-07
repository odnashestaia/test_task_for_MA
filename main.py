from src import get_metro_products, refactor_products, save_data, STOCKS, check_data


def main() -> None:
    """Основной скрипт программы для парсинга данных."""

    print('Получение данных с сайта METRO...')
    products = []
    checked_list = check_data()
    for stock in STOCKS:
        products.extend(refactor_products(get_metro_products(stock)))
    new_products = [product for product in products if product not in checked_list]
    checked_list.extend(new_products)
    save_data(checked_list)
    print('Парсинг завершен. Файл с данными сохранен в data/products.json')


if __name__ == '__main__':
    main()
