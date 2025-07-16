import psycopg2
from bs4 import BeautifulSoup
import requests
conn = psycopg2.connect(
    host='localhost',
    port='5432',
    dbname='postgres',
    user='postgres',
    password='' #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
)

cursor = conn.cursor()


url = "https://sudar.su/catalog/jackets/" #ссылка на сайт

def parse_insert():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #считывание сайта

    img_pictures = soup.find_all('img') #поиск картинок
    picture_id = 0
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
        cursor.execute("INSERT INTO sudar_jackets (image_id, image_url) VALUES (%s, %s)", (picture_id, strg)) #загрузка в таблицу
        conn.commit()
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
        cursor.execute("INSERT INTO sudar_jackets (image_id, image_url) VALUES (%s, %s)",
                       (picture_id, strg))  # загрузка в таблицу
        conn.commit()
        picture_id += 1

parse_insert()

cursor.close()
conn.close()
