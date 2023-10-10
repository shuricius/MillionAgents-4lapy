from requests import Session
from requests.exceptions import RequestException
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from random import randint
from time import sleep
from hashlib import md5
import config


result_parsing = list()


def init_excel():
    workbook = Workbook()
    sheet = workbook.active

    sheet.append(config.headers_excel)

    header_row = sheet[1]
    header_font = Font(bold=True, size=14)
    header_alignment = Alignment(horizontal='center')
    for cell in header_row:
        cell.font = header_font
        cell.alignment = header_alignment

    sheet.title = config.name_table

    return workbook, sheet


def generation_fingerprint(city):
    sess = Session()

    cookies = {
        'selected_city_code': city[0],
    }

    headers = {
        'Host': '4lapy.ru',
        'User-Agent': 'v4.1.3(Android 9, Asus ASUS_I005DA)',
        'Version-Build': '183',
        'Authorization': 'Basic NGxhcHltb2JpbGU6eEo5dzFRMyhy',
        'X-Apps-Build': '4.1.3(183)',
        'X-Apps-Os': '9',
        'X-Apps-Screen': f'{randint(800, 1920)}x{randint(600, 1080)}',
        'X-Apps-Device': 'Asus ASUS_I005DA',
        'X-Apps-Location': f'lat:{city[1]},lon:{city[2]}',
        'X-Apps-Additionally': '404',
        'Connection': 'close',
    }

    token = sess.get('https://4lapy.ru/api/start/',
                     headers=headers, cookies=cookies,
                     timeout=config.maximum_expectation, proxies=config.proxy)

    return sess, token.json()['data']['token'], headers, cookies


def get_sign(data):
    elements = [md5(str(i).encode()).hexdigest() for i in data.values()]
    elements.sort()
    return md5(('ABCDEF00G' + ''.join(elements)).encode()).hexdigest()


def parsing(category, city, city_parameters):
    sess, token, headers, cookies = None, None, None, None
    count_retry, page_products = 0, 1
    count_requests_fingerprint, count_requests_rotation = 0, 0

    while count_retry < config.max_error_retry:

        try:

            if not sess:
                sess, token, headers, cookies = generation_fingerprint(city_parameters)

            params = {
                'sort': 'popular',
                'category_id': category,
                'page': page_products,
                'count': config.requested_quantity_products,
                'token': token,
            }

            params['sign'] = get_sign(params)

            response = sess.get('https://4lapy.ru/api/goods_list_cached/',
                                params=params, cookies=cookies, headers=headers,
                                timeout=config.maximum_expectation, proxies=config.proxy).json()

            add_products = 0
            for product in response['data']['goods']:
                try:

                    if product['availability'] == 'В наличии':
                        add_products += 1
                        table.append([
                            product['id'],
                            product['title'],
                            product['webpage'],
                            product['price']['actual'],
                            product['price']['old'],
                            product['brand_name'],
                            city,
                        ])
                except:
                    pass

            print(f'added products - {add_products} | page - {page_products} | city - {city} | category - {category}')

            if page_products >= response['data']['total_pages']:
                return
            else:
                page_products += 1

            count_requests_fingerprint += 1
            count_requests_rotation += 1

            if count_requests_rotation == config.count_requests_rotation and config.rotation_proxy:
                try:
                    sess.get(config.rotation_proxy)
                    count_requests_rotation = 0
                    print('-- Rotation successfully')
                except Exception as error_rotation:
                    print(f'-- Error rotation - {error_rotation}')

            if count_requests_fingerprint == config.count_requests_generate_fingerprint:
                try:
                    sess, token, headers, cookies = generation_fingerprint(city_parameters)
                    count_requests_fingerprint = 0
                    print('-- Generation fingerprint successfully')
                except Exception as error_fingerprint:
                    print(f'-- Error generation fingerprint - {error_fingerprint}')

            count_retry = 0
            book.save(config.result_name_book)

        except RequestException:
            print('Error Connection - continue')

        except Exception:
            count_retry += 1
            print(f'-- Error requests - {count_retry}/{config.max_error_retry}')

        finally:
            sleep(config.timeout_requests)


def start_parsing():
    for category in config.categories:
        for city, city_parameters in config.cities.items():
            parsing(category, city, city_parameters)


if __name__ == "__main__":
    book, table = init_excel()

    start_parsing()
