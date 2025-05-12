import asyncio
import logging
import sqlite3
from datetime import datetime
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
import requests

bot = Bot(token='7630689498:AAG3HIYLI45_c1CACOQWrUcl4bSZOTimyeE')
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
token_API = '60b38f9ab0abb04092db9e20c61e3f20'


def init_db():
    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            city TEXT,
            temp INTEGER,
            request_time TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Отправь мне свою геолокацию, и я верну тебе координаты.\n\n"
        "Как отправить геолокацию:\n"
        "1. Нажми на скрепку (вложения)\n"
        "2. Выбери 'Геопозиция'\n"
        "3. Выбери 'Отправить мою текущую геопозицию' или укажи место на карте")

@dp.message(F.location)
async def handle_location(message: types.Message):
    location = message.location
    lat = location.latitude
    lon = location.longitude
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token_API}').json()
    city = response['name']
    temp = int(response['main']['temp']) - 273

    conn = sqlite3.connect('weather_bot.db')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO user_requests (user_id, city, temperature, request_time)
        VALUES (?, ?, ?, ?)
                   ''', (message.from_user.id, city, temp, datetime.now()))
    conn.commit()
    conn.close()
    description = response['weather'][0]['description']
    humidity = response['main']['humidity']
    feels_like = int(response['main']['feels_like'])-273
    wind_speed = response['wind']['speed']
    temp_min = int(response['main']['temp_min']) - 273
    temp_max = int(response['main']['temp_max']) - 273
    weather_report = (
            f"   <b>Погода в {city}</b>\n\n"
            f"🌡 <b>Температура:</b> {temp}°C (ощущается как {feels_like}°C)\n"
            f"💧 <b>Влажность:</b> {humidity}%\n"
            f"🌬 <b>Ветер со скоростью:</b> {wind_speed} м/с\n"
            f"📝 <b>Описание:</b> {description}\n\n"
            f"🌡 <b>Минимальная температура:</b> {temp_min}°C\n"
            f"🌡 <b>Максимальная температура:</b> {temp_max}°C\n"
            f"<i>Обновлено: {datetime.now().strftime('%H:%M %d.%m.%Y')}</i>"

        )
    await message.answer(weather_report, parse_mode='HTML')

async def main():
    init_db()
    print('Бот запущен')
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())