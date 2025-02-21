from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import asyncio

# Замените на токен вашего бота
API_TOKEN = '7561904095:AAFmcA68_Y7vgOjiPnjXiKxUR28idE6_pCM'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Логирование
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Это ваш Telegram Mini App.")

# Функция для запуска бота
def start_bot():
    executor.start_polling(dp, skip_updates=True)

# Запуск бота в отдельном потоке
if __name__ == '__main__':
    start_bot()