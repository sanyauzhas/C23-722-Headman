import psycopg2
from bs4 import BeautifulSoup
import requests
conn = psycopg2.connect( #для связи с таблицей
    host='localhost',
    port= '5432',
    dbname='postgres',
    user='postgres',
    password='pass'
)

cursor = conn.cursor()


url = "https://sudar.su/catalog/jackets/" #ссылка на сайт

def parse_insert():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #считывание сайта

    img_pictures = soup.find_all('img') #поиск картинок

    for img in range(len(img_pictures)):
        picture_url = img_pictures[img]['src']
        picture_id = img+1 #ID картинок
        with open(f'../images','wb') as f:
            if 'https' not in picture_url: #корректировка ссылок
                strg = 'https://sudar.su' + str(picture_url)
                g = requests.get(strg)
            else:
                g = requests.get(picture_url)
            with open(f'images/img'+str(picture_id)+'.jpg','wb') as d:
                d.write(g.content) #загрузка в папку 
        cursor.execute("INSERT INTO sudar_jackets (image_id, image_url) VALUES (%s, %s)", (picture_id, picture_url)) #загрузка в таблицу
        conn.commit()

parse_insert()

cursor.close()
conn.close()
