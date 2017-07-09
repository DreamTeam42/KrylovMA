import requests
import json
from bs4 import BeautifulSoup

def parse(url, type):

    list = {}
    list['Тип объявления'] = type

    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    zagolovok = soup.find('div', class_='cols__wrapper')

    zagolovoch = zagolovok.find('h1', class_='hdr__inner').text
    list['Заголовок'] = zagolovoch

    adress = zagolovok.find('span', class_='hdr__inner').text
    list['Адресс'] = adress

    prodav = soup.find('span', class_='p-contact__name').text.replace('\"', '')
    list['Контактное лицо'] = prodav

    phone = soup.find('span', class_='valign_middle').text + "28"
    list['Телефон'] = phone

    data = soup.find('span', class_='note__text js-ago').text
    list['Дата публикации и обновления объявления'] = data

    tablel = soup.find('div',  class_='cols__column cols__column_small_12 cols__column_medium_12 cols__column_large_12')
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
        etaz = soup.findAll('span', {'class': 'p-params__text'})[0].text.replace('/', ' из ')
        list['Этаж'] = etaz
    except:
        list['Этаж'] = "Не указано"

    try:
        colvo_room = soup.findAll('span', {'class': 'p-params__text'})[1].text
        list['Количество комнат'] = colvo_room
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

    promezutok = soup.find('div', { 'class': 'cols__column cols__column_small_19 cols__column_medium_30 cols__column_large_34 js-track_visibility'})
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

def getPageCount(html):
    rrr = requests.get(html)
    soup = BeautifulSoup(rrr.text, 'html.parser')
    paggination = soup.find('div', class_='paging js-paging')
    return int(paggination.find_all('a')[-1].text)

def scanPage(url):
    html1 = requests.get(url)
    soup1 = BeautifulSoup(html1.text, 'html.parser')
    offerURLs = soup1.findAll("a", {"class": "p-instance__title link-holder"})
    i=0
    while (i!= 15):
        for item in offerURLs:
            href = item.attrs["href"]
            type = "Продажа"
            #print("Начинаю парсить " + str(href))
            descArr.append(parse(href, type))
            i+=1

def scanSection(url):
    #html2 = requests.get(url)
    #soup2 = BeautifulSoup(html2.text, 'html.parser')
    pageCount = (getPageCount(url))
    print('Всего страниц найдено %d' % pageCount)
    for page in range(1, pageCount):
        print('Парсинг %d%%' % (page / pageCount * 100))
        https = (url + '?page=%d' % page)
        descArr.append(scanPage(https))

if __name__ == '__main__':
    descArr = []
    exampleURL = "https://vlgg.realty.mail.ru/sale/living/"
    scanSection(exampleURL)
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(descArr, file, indent=2, ensure_ascii=False)