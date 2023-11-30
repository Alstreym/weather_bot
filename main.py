import telebot
import requests
import json

bot = telebot.TeleBot('6784398744:AAENsR0ur7YMeYUh-XPwsszSVaHZxkOFWO0')
API = 'bc39019bf53eaa9529ac0b1e7a197b50'

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, напиши название города')

@bot.message_handler(content_types=['text']) #отслеживаем текст который ввел пользователь

def get_weather(message):
    city = message.text.strip().lower()    #strip позволяет удалить пробелы до и после самой строки
    #lower - нижний регистр
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        wind_speed = data["wind"]["speed"]
        feel_like = data["main"]["feels_like"]
        cloudiness = data["clouds"]["all"]
        degree_symbol = "\u00B0"
        response_message = f'Сейчас погода: {temp}{degree_symbol}\nСкорость ветра: {wind_speed} м/с\nОщущается как: {feel_like}{degree_symbol}'
        bot.reply_to(message, response_message)

        image = 'free-icon-sun-rays-3385807.png' if temp > 5.0 and cloudiness < 50 else 'free-icon-cloudy-1146869.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)

        image1 = 'free-icon-clouds-4724093.png' if cloudiness > 50 and temp < 5.0 else 'free-icon-sun-rays-3385807.png'
        file = open('./' + image1, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан неверно!')
bot.polling(none_stop=True)
