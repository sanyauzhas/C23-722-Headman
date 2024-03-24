import psycopg2
from bs4 import BeautifulSoup
import requests
conn = psycopg2.connect(
    host='localhost',
    port= '5432',
    dbname='postgres',
    user='postgres',
    password='pass'
)

cursor = conn.cursor()


url = "https://sudar.su/catalog/jackets/"

def scrape_and_insert():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_elements = soup.find_all('img')

    for img in range(len(img_elements)):
        picture_url = img_elements[img]['src']
        user_id = img+1
        with open(f'../images','wb') as f:
            if 'https' not in picture_url:
                strg = 'https://sudar.su' + str(picture_url)
                g = requests.get(strg)
            else:
                g = requests.get(picture_url)
            with open(f'images/img'+str(user_id)+'.jpg','wb') as d:
                d.write(g.content)
        cursor.execute("INSERT INTO sudar_jackets (image_id, image_url) VALUES (%s, %s)", (user_id, picture_url))
        conn.commit()

scrape_and_insert()

cursor.close()
conn.close()