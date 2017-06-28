import requests
from bs4 import BeautifulSoup

#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 YaBrowser/17.6.0.1633 Yowser/2.5 Safari/537.36'}
URL = "https://vlgg.realty.mail.ru/offer/sale-liv-61027030014258681.html"
page = requests.get(URL)
pageContent = page.content
soup = BeautifulSoup(pageContent, "html.parser")
price = soup.find("span", {"class": "priceelem"})


print(price)
#print (soup.prettify()) #Вывод дерева