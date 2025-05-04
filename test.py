import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# Токен вашего бота
BOT_TOKEN = "8088057543:AAGlEh3GDQvSYLuB7OH23QRQRo1-YC7DsUU"

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота с новым способом установки parse_mode
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Отправь мне свою геолокацию, и я верну тебе координаты.\n\n"
        "Как отправить геолокацию:\n"
        "1. Нажми на скрепку (вложения)\n"
        "2. Выбери 'Геопозиция'\n"
        "3. Выбери 'Отправить мою текущую геопозицию' или укажи место на карте"
    )

# Обработчик геолокации
@dp.message(F.location)
async def handle_location(message: Message):
    location = message.location
    latitude = location.latitude
    longitude = location.longitude
    
    await message.answer(
        f"🌍 Координаты получены:\n"
        f"Широта: <code>{latitude}</code>\n"
        f"Долгота: <code>{longitude}</code>\n\n"
        f"Ссылка на Google Maps: "
        f"https://www.google.com/maps?q={latitude},{longitude}"
    )

# Обработчик сообщений без геолокации
@dp.message()
async def handle_other_messages(message: Message):
    await message.answer("Пожалуйста, отправьте мне вашу геолокацию.")

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())