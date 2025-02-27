from django.core.management.base import BaseCommand
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()
import os
from telebot import TeleBot


# Объявление переменной бота
bot = TeleBot(settings.os.getenv('BOT_KEY'), threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    @bot.message_handler(commands=['start'])
    def start_message(message):
        your_variable = message.from_user.id

    