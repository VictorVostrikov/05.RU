import csv
import sys
from datetime import date

import requests
from tqdm import tqdm

# записи кукисов хедеров и параметров из cUrl converter

cookies = {
    'versionNumber': '1',
    'user-lists': '%7B%22userLists%22%3A%7B%22user%22%3A%7B%22compare%22%3A%7B%7D%2C%22favorite%22%3A%7B%7D%2C%22cart%22%3A%7B%7D%7D%2C%22guest%22%3A%7B%22compare%22%3A%7B%7D%2C%22favorite%22%3A%7B%7D%2C%22cart%22%3A%7B%7D%7D%7D%7D',
    'exp-accessories': 'CXRA1HX9SSqlVRR3pdHMPA.0',
    'SERV': 'vue1',
    'showAppPromo': 'false',
    'SERVERUSED': 'btx-01',
    'popmechanic_sbjs_migrations': 'popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1',
    'nuxt-vue-store': '%7B%22user%22%3A%7B%22data%22%3Anull%7D%2C%22location%22%3A%7B%22currentCity%22%3A%7B%22id%22%3A1359%2C%22code%22%3A%220000495241%22%2C%22name%22%3A%22%D0%9C%D0%B0%D1%85%D0%B0%D1%87%D0%BA%D0%B0%D0%BB%D0%B0%22%2C%22lat%22%3A42.983024%2C%22lon%22%3A47.504872%2C%22region%22%3A%7B%22name%22%3A%22%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%94%D0%B0%D0%B3%D0%B5%D1%81%D1%82%D0%B0%D0%BD%22%2C%22id%22%3A37%7D%7D%2C%22confirmed%22%3Atrue%7D%2C%22token%22%3A%7B%22accessToken%22%3A%7B%22value%22%3A%220473f6ec-6195-11ed-8a9c-2e238dd6ce4a%22%2C%22expire%22%3A1670744817%7D%2C%22refreshToken%22%3A%7B%22value%22%3A%2204746613-6195-11ed-8a9c-2e238dd6ce4a%22%2C%22expire%22%3A1670744817%7D%7D%7D',
    'ABOT': 'd82142bf3b0d307ea40c30ac1e2effca',
}

headers = {
    'authority': '05.ru',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'authorization': 'Bearer 0473f6ec-6195-11ed-8a9c-2e238dd6ce4a',
    # Requests sorts cookies= alphabetically
    # 'cookie': 'versionNumber=1; user-lists=%7B%22userLists%22%3A%7B%22user%22%3A%7B%22compare%22%3A%7B%7D%2C%22favorite%22%3A%7B%7D%2C%22cart%22%3A%7B%7D%7D%2C%22guest%22%3A%7B%22compare%22%3A%7B%7D%2C%22favorite%22%3A%7B%7D%2C%22cart%22%3A%7B%7D%7D%7D%7D; exp-accessories=CXRA1HX9SSqlVRR3pdHMPA.0; SERV=vue1; showAppPromo=false; SERVERUSED=btx-01; popmechanic_sbjs_migrations=popmechanic_1418474375998%3D1%7C%7C%7C1471519752600%3D1%7C%7C%7C1471519752605%3D1; nuxt-vue-store=%7B%22user%22%3A%7B%22data%22%3Anull%7D%2C%22location%22%3A%7B%22currentCity%22%3A%7B%22id%22%3A1359%2C%22code%22%3A%220000495241%22%2C%22name%22%3A%22%D0%9C%D0%B0%D1%85%D0%B0%D1%87%D0%BA%D0%B0%D0%BB%D0%B0%22%2C%22lat%22%3A42.983024%2C%22lon%22%3A47.504872%2C%22region%22%3A%7B%22name%22%3A%22%D0%A0%D0%B5%D1%81%D0%BF%D1%83%D0%B1%D0%BB%D0%B8%D0%BA%D0%B0%20%D0%94%D0%B0%D0%B3%D0%B5%D1%81%D1%82%D0%B0%D0%BD%22%2C%22id%22%3A37%7D%7D%2C%22confirmed%22%3Atrue%7D%2C%22token%22%3A%7B%22accessToken%22%3A%7B%22value%22%3A%220473f6ec-6195-11ed-8a9c-2e238dd6ce4a%22%2C%22expire%22%3A1670744817%7D%2C%22refreshToken%22%3A%7B%22value%22%3A%2204746613-6195-11ed-8a9c-2e238dd6ce4a%22%2C%22expire%22%3A1670744817%7D%7D%7D; ABOT=d82142bf3b0d307ea40c30ac1e2effca',
    'dnt': '1',
    'referer': 'https://05.ru/catalog/audio-video/tv/',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

params = {
    'reviews_size': '2',
    'questions_size': '2',
    'not_load': 'BASKET_AMOUNT,IN_BASKET,IN_FAVORITES,IN_COMPARE',
    'code': '1',
}


# ниже изыскания откуда брать и подставлять запросы json
# # продукт
# # https://05.ru/catalog/audio-video/tv/193175/ пример ссылки на продукт
#
# response = requests.get('https://05.ru/api/v1/catalog/products/164655', params=params, cookies=cookies, headers=headers).json()
# with open('product.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, indent=4, ensure_ascii=False)
#
#
# # каталог ТВ
# # ссылка на каталог https://05.ru/catalog/audio-video/
#
# response = requests.get('https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Faudio-video%2F', params=params, cookies=cookies, headers=headers).json()
# with open('catalog.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, indent=4, ensure_ascii=False)
#
#
#
# # каталог ТВ LG
# # ссылка на каталог https://05.ru/catalog/audio-video/tv/lg/
#
# response = requests.get('https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Faudio-video%2Ftv%2Flg%2F%3Fsize%3D60', params=params, cookies=cookies, headers=headers).json()
# with open('catalogLG.json', 'w', encoding='utf-8') as file:
#     json.dump(response, file, indent=4, ensure_ascii=False)
#
# https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Fcomputers%2Faccessories%2F%3Fsize%3D60  https://05.ru/catalog/computers/accessories/
# https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Faudio-video%2Ftv%2F%3Fsize%3D60   https://05.ru/catalog/audio-video/tv/
# https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Fappliance%2Fkbt%2F%3Fpage%3D5%26size%3D60
# https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Fappliance%2Fkbt%2F%3Fpage%3D12%26size%3D60
# https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2Fappliance%2Fkbt%2F%3Fpage%3D1%26size%3D60


# struct = time.localtime()
# mon = struct.tm_mon
# year = struct.tm_year
# day = struct.tm_mday


def out_red(text):
    print("\033[32m{}".format(text))

# строка на вход в виде https://05.ru/catalog/portativ/phones/ берется с сайта
cat = input("Укажите каталог: ")
pagen = 0
group = cat.split('/')[-3]
undergroup = cat.split('/')[-2]

# создаем файл первой страницы каталога
url = f'https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2F{group}%2F{undergroup}%2F%3Fpage%3D1%26size%3D60'

response = requests.get(url=url, params=params, cookies=cookies, headers=headers)
data = response.json()

strcsv = []
dimcode = []
product_url = []
current_date = date.today()

# создаем json из названия группы товара и подгруппы, данные берем из введенного каталога

print('Текущая страница: ', data['result']['PRODUCTS_BLOCK']['PAGINATION']['CURRENT'])
print('Всего страниц каталога: ', data['result']['PRODUCTS_BLOCK']['PAGINATION']['COUNT'])
print('Количество продуктов в каталоге: ', data['result']['PRODUCTS_BLOCK']['PAGINATION']['ROWS'])
pagen = int(data['result']['PRODUCTS_BLOCK']['PAGINATION']['COUNT'])

res = [['Код товара', 'Группа', 'Категория', 'Название', 'Цена', 'Старая цена', 'Бонус', 'Сток in City', 'Сток Amnt']]

# итерации по всем созданный файлам и сбор данных
out_red('Загружаю загловки и продукцию...')

for page in tqdm(range(1, int(pagen + 1))):
    url = f'https://05.ru/api/v1/snippets/vue/catalog?seo_link=%2Fcatalog%2F{group}%2F{undergroup}%2F%3Fpage%3D{page}%26size%3D60'
    response = requests.get(url=url, params=params, cookies=cookies, headers=headers)
    data = response.json()

    # записываем в csv
    try:
        for p in data['result']['PRODUCTS_BLOCK']['ITEMS']:
            code = p['CODE']
            name = p['NAME']
            bonus = [price['BONUS'] for price in p['PRICES'] if price['CODE'] == "DEFAULT"]
            old_price = [price['PRINT_PRICE'] for price in p['PRICES'] if price['CODE'] != "DEFAULT"]
            category = p['SECTION']['NAME']
            amount = p['AMOUNT']['IN_CURRENT_CITY']
            amount_all = p['AMOUNT']['ALL']
            groupcat = p['SECTION']['PARENT_NAME']
            price = [price['PRINT_PRICE'] for price in p['PRICES'] if price['CODE'] != "PROMO"]

            flatten = code, groupcat, category, name, str(price).replace("['", '').replace("']", '').replace("[]", ''), \
                      str(old_price).replace("['", '').replace("']", '').replace("[]", ''), str(bonus).replace("[",
                                                                                                               '').replace(
                "]", '').strip(), amount, amount_all
            res.append(flatten)
    except Exception:
        print(
            f'\nНесколько продуктов не имеют описания, не распаковываются\n'
            f'Пока выкинем их для достоверности остальных данных\n')
        continue

    with open(f'05.RU_{group}_{undergroup}_{current_date}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(res)

out_red(f'05.RU_{group}_{undergroup}_{current_date}.csv сохранен в папке с приложением')

input("Нажмите Enter.....")
sys.exit()
