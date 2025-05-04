import asyncio
import logging
from aiogram import Dispatcher, Bot, types, F
from aiogram.filters.command import Command
import requests
import json

bot = Bot(token='7630689498:AAG3HIYLI45_c1CACOQWrUcl4bSZOTimyeE')
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()
token_API = '60b38f9ab0abb04092db9e20c61e3f20'


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")

@dp.message(F.location)
async def handle_location(message: types.Message):
    location = message.location
    lat = location.latitude
    lon = location.longitude
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={token_API}').json()
    city = response['name']
    temperature = int(response['main']['temp']) - 273
    weather = response['weather'][0]['description']
    humidity = response['main']['humidity']
    feelslike = int(response['main']['feels_like'])-273
    speed = response['wind']['speed']
    # await message.answer(f"Широта {location.latitude} \n Долгота:{location.longitude} \nГород:{city} \nТемпература:{temperature}° \n")
    await message.answer(f"Город:{city} \nТемпература:{temperature}° \nСостояние:{weather} \nВлажность:{humidity} \nОщущается как:{feelslike}°\nСкорость ветра:{speed}м/с")


async def main():
    print('Бот запущен')
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())