from bs4 import BeautifulSoup
import requests
import time
import json
import re

#URL = "https://vlgg.realty.mail.ru/sale/living/"
URL = "https://vlgg.realty.mail.ru/offer/sale-liv-1946920318042940.html?osale1"


def get_page_count(html):
    rrr = requests.get(html)
    soup = BeautifulSoup(rrr.text, 'html.parser')
    paggination = soup.find('div', class_='paging js-paging')
    return int(paggination.find_all('a')[-1].text)

def main():
    #page_count = (get_page_count(URL))
    lis = parse(URL)
    print (lis)
#progects = []
"""
    for page in range(1, page_count):
        print('Parse %d%%' %(page/page_count * 100))
        progects.extend(parse(requests.get(URL2 = URL + '?page=%d' % page)))

        #rrr = requests.get(URL2)
        #soup = BeautifulSoup(rrr.text, 'html.parser')"""


def parse(url):
    list = {}
    #list['Тип объявления'] = type

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    zagolovok = soup.find('div', class_='cols__wrapper')

    # room = zagolovok.find('h1', class_='hdr__inner').text
    # list['Количество комнат'] = room

    adress = zagolovok.find('span', class_='hdr__inner').text
    list['Адресс'] = adress

    prodav = soup.find('span', class_='p-contact__name').text
    list['Контактное лицо'] = prodav

    phone = soup.find('span', class_='valign_middle').text + "28"
    list['Телефон'] = phone

    data = soup.find('span', class_='note__text js-ago').text
    list['Дата публикации и обновления объявления'] = data

    tablel = soup.find('div', class_='cols__column cols__column_small_12 cols__column_medium_12 cols__column_large_12')
    table = tablel.find('div', class_='cols__inner')

    price = table.find('span', class_='hdr__inner').text.replace('\xa0', ' ')
    list['Цена'] = price

    try:
        price_for_m = table.find('span', class_='note__text').text.replace('\xa0', ' ')
        list['Цена за м2'] = price_for_m
    except:
        list['Цена за м2'] = "Не указано"

    try:
        district = table.find('span', class_='link__text').text.strip()
        list['Район'] = district
    except:
        list['Район'] = "Не указано"

    try:
        district = soup.findAll('span', {'class': 'p-params__text'})[0].text.replace('/', ' из ')
        list['Этаж'] = district
    except:
        list['Этаж'] = "Не указано"

    try:
        district = soup.findAll('span', {'class': 'p-params__text'})[1].text
        list['Количество комнат'] = district
    except:
        list['Количество комнат'] = "Не указано"

    try:
        ploshad_o = soup.findAll('span', {'class': 'p-params__text'})[2].text
        list['Общая площадь'] = ploshad_o
    except:
        list['Общая площадь'] = "Не указано"

    try:
        ploshad_z = soup.findAll('span', {'class': 'p-params__text'})[3].text
        list['Жилая площадь'] = ploshad_z
    except:
        list['Жилая площадь'] = "Не указано"

    try:
        ploshad_k = soup.findAll('span', {'class': 'p-params__text'})[4].text
        list['Площадь кухни'] = ploshad_k
    except:
        list['Площадь кухни'] = "Не указано"

    promezutok = soup.find('div', {
        'class': 'cols__column cols__column_small_19 cols__column_medium_30 cols__column_large_34 js-track_visibility'})
    try:
        opisanie = promezutok.find('div', {'class': ''}).text
        list['Описание'] = opisanie
    except:
        list['Описание'] = "Не указано"

    vyrez = soup.findAll('div', {'class': 'cols__wrapper'})[4]
    # print(vyrez)

    name = vyrez.findAll("span", {"class": "p-params__name color_gray"})
    value = vyrez.findAll("span", {"class": "p-params__text"})

    for i in name:
        for e in value:
            featureName = i
            featureValue = e
            list[''.join(featureName.get_text().encode(html.encoding).decode('utf-8'))] = ''.join(
                featureValue.get_text().encode(html.encoding).decode('utf-8'))
            del value[0]
            break

    return list


if __name__ == '__main__':
    main()
