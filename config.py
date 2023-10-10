
headers_excel = ['id товара', 'наименование', 'ссылка на товар', 'регулярная цена', 'промо цена', 'бренд', 'город']

name_table = 'Результаты парсинга'

result_name_book = "result.xlsx"

cities = {
    'Москва': ('0000073738', 55.755819, 37.617644),
    'Санкт-Петербург': ('0000103664', 59.939095, 30.315868)
}

categories = ('2',)  # корма для кошек

requested_quantity_products = '10'

proxy = None    # or {'http': 'proxy', 'https': 'proxy'}
rotation_proxy = None   # or link
count_requests_rotation = None  # or number

count_requests_generate_fingerprint = None    # or number

max_error_retry = 10

timeout_requests = 0.3

maximum_expectation = 30

