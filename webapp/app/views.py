from rest_framework import generics
from .models import Student, Interest, Like
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render, redirect
import telebot
from dotenv import load_dotenv
load_dotenv()
import os
from django.http import HttpResponse

bot = telebot.TeleBot(os.getenv('BOT_KEY'))

def index(request):
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.body.decode('utf-8'))
        bot.process_new_updates([update])

    return HttpResponse('<h1>Ты подключился!</h1>')

@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    name = ''
    if message.from_user.last_name is None:
        name = f'{message.from_user.first_name}'
    else:
        name = f'{message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, f'Привет! {name}\n'
                                      f'Я бот, который будет спамить вам беседу :)\n\n'
                                      f'Чтобы узнать больше команд, напишите /help')
    
    
# Webhook
bot.set_webhook(url="https://myapp.pythonanywhere.com/" + os.getenv('BOT_KEY'))

#def korpus_view(request):
#    return render(request, 'app/korpus.html')

class InterestListCreate(generics.ListCreateAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class InterestRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
 
class LikeListCreate(generics.ListCreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

class LikeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
