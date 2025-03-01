from rest_framework import generics
from .models import Student, Interest, Like
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv()
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



def index(request):
    return render(request, 'app/index.html')

def reg_page(request):
    return render(request, 'app/start.html')
def fio_page(request):
    return render(request, 'app/fio.hmtl')

class CheckIDView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')  # Получаем telegram_id из запроса
        if not telegram_id:
            return Response({'error': 'telegram_id не указан'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли студент с таким telegram_id
        if Student.objects.filter(telegram_id=telegram_id).exists():
            return Response({'status': 'error', 'message': 'ID существует в базе данных'})

        # Создаем нового студента с значениями по умолчанию
        Student.objects.create(
            telegram_id=telegram_id,
            name="Имя по умолчанию",  # Укажите значение по умолчанию
            campus="1",  # Укажите значение по умолчанию
            birth_year=2000,  # Укажите значение по умолчанию
            gender="male",  # Укажите значение по умолчанию
        )
        # Возвращаем JSON с URL для перенаправления
        return Response({'status': 'success', 'message': 'ID был занесен в базу данных', 'redirect_url': '/start/'})






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
