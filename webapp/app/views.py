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
from django.db import IntegrityError
import logging
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'app/index.html')
def reg_page(request):
    return render(request, 'app/start.html')

def fio_view(request):
    return render(request, 'app/fio.html')
def korpus_view(request):
    return render(request, 'app/korpus.html')
def god_view(request):
    return render(request, 'app/god.html')
def pol_view(request):
    return render(request, 'app/pol.html')
def interes_view(request):
    return render(request, 'app/interes.html')
def nastroika_view(request):
    return render(request, 'app/nastroika.html')
def success_view(request):
    return render(request, 'app/success.html')

class CheckIDView(APIView):
    def post(self, request):
        telegram_id = request.data.get('telegram_id')  # Получаем telegram_id из запроса
        if not telegram_id:
            return Response({'error': 'telegram_id не указан'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли студент с таким telegram_id
        student = Student.objects.filter(telegram_id=telegram_id).first()
        if student:
            # Если студент найден, возвращаем его данные
            serializer = StudentSerializer(student)
            return Response({'status': 'success', 'message': 'Вы вошли в аккаунт', 'data': serializer.data})
        else:
            # Если студент не найден, начинаем процесс регистрации
            return Response({'status': 'register', 'message': 'Начните регистрацию'})

class RegisterView(APIView):
    def post(self, request):
        try:
            telegram_id = request.data.get('telegram_id')
            if not telegram_id:
                return Response({'status': 'error', 'message': 'telegram_id не указан'}, status=status.HTTP_400_BAD_REQUEST)

            name = request.data.get('name')
            campus = request.data.get('campus')
            birth_year = request.data.get('birth_year')
            gender = request.data.get('gender')
            interests = request.data.get('interests', [])

            # Создаем нового студента
            student = Student.objects.create(
                telegram_id=telegram_id,
                name=name,
                campus=campus,
                birth_year=birth_year,
                gender=gender,
            )

            # Добавляем выбранные интересы
            for interest_id in interests:
                interest = Interest.objects.get(id=interest_id)
                student.interests.add(interest)

            return Response({'status': 'success', 'message': 'Данные успешно сохранены'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



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
