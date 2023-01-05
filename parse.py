from pprint import pprint
from pydoc import html
from bs4 import BeautifulSoup
import requests
from dbparse import krysha_parse_sql_orm
from selenium import webdriver



class Parse_Krysha:
    def __init__(self):
        self.HOST = HOST = "https://krisha.kz"
        self.URL = URL = "https://krisha.kz/arenda/kvartiry/almaty-almalinskij/?das[rent.period]=2"

        self.HEADERS = HEADERS = {
            'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
            "accept": "text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8" 
        }


    def get_html(self, url: str, params=' '):
        """ это функция получает данные из сайта """
        return requests.get(url, headers=self.HEADERS, params=params)

    
    def get_content(self, html):
        
        soup = BeautifulSoup(html.text, 'html.parser')
        items = soup.find_all('div', class_='a-card__inc')
        list_items = []
        for item in items:
            title = item.find('div', class_='a-card__header-left').find('a').get_text(strip=True)
            image = item.find('img').get('src')
            link = self.HOST + item.find('div', class_='a-card__header-left').find('a').get('href')
            price = item.find('div', class_='a-card__price').get_text(strip=True)
            address = item.find('div', class_='a-card__subtitle').get_text(strip=True)
            get_autor = self.get_html(url=link)
            soup_autor = BeautifulSoup(get_autor.text, 'html.parser')
            try:
                autor=soup_autor.find('div', class_='owners__item user-type-2  is-verified').find('div', 'owners__name').get_text(strip=True)
            except:
                autor=None
            # self.driver.get(get_autor)
            # btn = self.driver.find_element_by_css_selector('button[class="show-phones"]')
            # btn.click()

            list_items.append({
                'title':title,
                'image':image,
                'link':link,
                'price':price.replace('\xa0', '').replace('〒', ''),
                'address':address,
                'autor':autor
            })
        return list_items

    
    def save(items, path):
        with open(path, 'w') as file:
            for num, item in enumerate(items, 1):
                file.write(f"№{num} - Называние: {item['title']}\n")
                file.write(f"       - Ссылка: {item['link']}\n")
                file.write(f"       - Картинка:  {item['image']}\n")
                file.write(f"       - Цена: {item['price']}\n")
                file.write(f"       - Адрес: {item['address']}\n")
                file.write(f"       - Автор: {item['autor']}\n")

    

    def parse(self, page: int):
        list_data = []
        for pg in range(1, page + 1):
            html = self.get_html(url=self.URL, params={'page' : pg})
            if html.status_code == 200:    
                items = self.get_content(html)
                list_data.extend(items)
                print(f'Старнница {pg} готово!')
        self.save(list_data, 'krysha.txt')  
        print('Успешно сохронили все данные')
        return list_data
        
    def save_sql(self, page):
        list_data = []
        for pg in range(1, page + 1):
            html = self.get_html(url=self.URL, params={'page' : pg})
            if html.status_code == 200:    
                items = self.get_content(html=html)
                list_data.extend(items)
                print(f'Старнница {pg} готово!')
        for item in list_data:
            krysha_parse_sql_orm.register(name=item['title'], 
                            link=item['link'], 
                            image=item['image'], 
                            price=item['price'],
                            address=item['address'],
                            autor=item['autor'])
    
krysha_parse_orm = Parse_Krysha()
krysha_parse_orm.save_sql(3)
# krysha_parse_orm.parse(2)
# html = krysha_parse_orm.parse(1)
# print(ht