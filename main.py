import psycopg2
from bs4 import BeautifulSoup
import requests
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='postgres',
    user='postgres',
    password='pass' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
)

cursor = conn.cursor()


url = "https://sudar.su/catalog/jackets/" #ссылка на сайт

def parse_insert():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #считывание сайта
    img_pictures = soup.find_all('img') #поиск картинок
    picture_id = 0
    links = soup.find_all('a', class_='js-product-link-to-detail')
    for img in range(0,5):
        picture_url = img_pictures[img]['src']
        with open(f'../images','wb') as f:
            if 'https' not in picture_url: #корректировка ссылок
                strg = 'https://sudar.su' + str(picture_url)
                g = requests.get(strg)
            else:
                g = requests.get(picture_url)
                strg = picture_url
            with open(f'images/img'+str(picture_id)+'.jpg','wb') as d:
                d.write(g.content) #загрузка в папку
        picture_id += 1
    for img in range(6, len(img_pictures),2):
        picture_url = img_pictures[img]['src']
        with open(f'../images', 'wb') as f:
            if 'https' not in picture_url:  # корректировка ссылок
                strg = 'https://sudar.su' + str(picture_url)
                g = requests.get(strg)
            else:
                g = requests.get(picture_url)
                strg = picture_url
            with open(f'images/img' + str(picture_id) + '.jpg', 'wb') as d:
                d.write(g.content)  # загрузка в папку
        str_url = 'https://sudar.su' + links[picture_id-5]['href']
        response2 = requests.get(str_url)
        soup2 = BeautifulSoup(response2.text,'html.parser')
        name = soup2.find('h1', itemprop="name")
        price = soup2.find('div', class_="b-price m-item-price")
        description = soup2.find('p', itemprop="description")
        cursor.execute("INSERT INTO sudar_jackets (image_id, image_url,product_url,product_name,product_price,product_desc) VALUES (%s, %s, %s, %s, %s, %s)",
                       (picture_id-4, strg,str_url,name.text,price.text,description.text))  # загрузка в таблицу
        conn.commit()
        picture_id += 1

parse_insert()

cursor.close()
conn.close()
