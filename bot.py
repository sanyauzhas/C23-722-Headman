import random
import telebot
import psycopg2
from telebot import types
import webbrowser

token = '6885878989:AAE_XaZLdQqBA-I8PHxvsVoGiaq4kAl-kUQ'
bot = telebot.TeleBot(token)
url = "https://sudar.su/catalog/jackets/"


@bot.message_handler(commands=['start'])
def start(m, res=False):
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.InlineKeyboardButton(text="Случайный товар")
        item2=types.InlineKeyboardButton(text="Открыть каталог")
        keyboard.add(item1)
        keyboard.add(item2)
        bot.send_message(m.chat.id, '<b>Вас приветствует парсинг-бот магазина "Сударь". Пришлите номер товара или нажмите кнопку ниже</b>', parse_mode = 'html', reply_markup=keyboard)


@bot.message_handler()
def handle_id(message):
    if message.text.strip() == 'Случайный товар':
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            dbname='postgres',
            user='postgres',
            password='pass'
        )
        cursor = conn.cursor()
        id = random.randint(1, 20)
        str_id = str(id)
        cursor.execute("SELECT image_url, product_name, product_price, product_desc, product_url FROM sudar_jackets WHERE image_id = %s", (str_id,))
        result = cursor.fetchone()
        image_url = result[0]
        name = result[1]
        price = result[2]
        description = result[3]
        product_url = result[4]
        bot.send_photo(message.chat.id, image_url)
        bot.send_message(message.chat.id, name)
        bot.send_message(message.chat.id, price)
        bot.send_message(message.chat.id, description)
        bot.send_message(message.chat.id, product_url)
    elif message.text.strip() == 'Открыть каталог':
        webbrowser.open(url)
    else:
        user_input = message.text.strip()

        conn = psycopg2.connect(
            host='localhost',
            port= '5432',
            dbname='postgres',
            user='postgres',
            password='pass'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT image_url, product_name, product_price, product_desc, product_url FROM sudar_jackets WHERE image_id = %s", (user_input,))
        result = cursor.fetchone()
        if result:
            image_url = result[0]
            name = result[1]
            price = result[2]
            description = result[3]
            product_url = result[4]
            bot.send_photo(message.chat.id, image_url)
            bot.send_message(message.chat.id, name)
            bot.send_message(message.chat.id, price)
            bot.send_message(message.chat.id, description)
            bot.send_message(message.chat.id, product_url)
        else:
            bot.send_message(message.chat.id, 'Такого товара нет')
        cursor.close()
        conn.close()


if __name__ == "__main__":
    bot.polling(none_stop=True)
