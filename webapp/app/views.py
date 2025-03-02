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
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

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
            # Если студент найден, возвращаем его данные и telegram_id
            serializer = StudentSerializer(student)
            return Response({
                'status': 'success',
                'message': 'Вы вошли в аккаунт',
                'data': serializer.data,
                'telegram_id': telegram_id  # Добавляем telegram_id в ответ
            })
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
            interest_names = request.data.get('interests', [])  # Получаем названия интересов

            # Создаем нового студента
            student = Student.objects.create(
                telegram_id=telegram_id,
                name=name,
                campus=campus,
                birth_year=birth_year,
                gender=gender,
            )

            # Добавляем выбранные интересы
            for interest_name in interest_names:
                interest, created = Interest.objects.get_or_create(name=interest_name)
                student.interests.add(interest)

            return Response({'status': 'success', 'message': 'Данные успешно сохранены'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def success_view(request):
    # Получаем telegram_id из параметров URL
    telegram_id = request.GET.get('telegram_id')

    if not telegram_id:
        return render(request, 'app/success.html', {'error': 'Telegram ID не указан'})

    # Ищем студента в базе данных
    student = get_object_or_404(Student, telegram_id=telegram_id)

    # Получаем все интересы студента
    interests = student.interests.all()

    # Передаем данные в шаблон
    context = {
        'student': student,
        'interests': interests,
    }
    return render(request, 'app/success.html', context)

def delete_account(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')  # Получаем telegram_id из запроса

        if not telegram_id:
            return JsonResponse({'status': 'error', 'message': 'Telegram ID не указан'}, status=400)

        # Ищем студента в базе данных
        student = get_object_or_404(Student, telegram_id=telegram_id)

        # Удаляем студента
        student.delete()

        return JsonResponse({'status': 'success', 'message': 'Аккаунт успешно удален'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Недопустимый метод запроса'}, status=405)

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
