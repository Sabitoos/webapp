from django.apps import AppConfig
import threading
from bot import start_bot  # Импортируем функцию запуска бота

class webappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        # Запускаем бота в отдельном потоке при старте Django
        bot_thread = threading.Thread(target=start_bot)
        bot_thread.daemon = True  # Поток завершится при завершении основного процесса
        bot_thread.start()