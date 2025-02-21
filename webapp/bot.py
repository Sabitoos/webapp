from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
import logging
import asyncio

# Замените на токен вашего бота
API_TOKEN = '7561904095:AAFmcA68_Y7vgOjiPnjXiKxUR28idE6_pCM'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)  # Указываем режим парсинга (HTML или Markdown)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Это ваш Telegram Mini App.")

# Асинхронная функция для запуска бота
async def start_bot():
    await dp.start_polling(bot)

# Запуск бота
if __name__ == '__main__':
    asyncio.run(start_bot())