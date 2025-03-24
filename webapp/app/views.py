from rest_framework import generics
from .models import Student, Interest, Like
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv()
from django.contrib import messages
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
from django.core.files.storage import default_storage
from django.conf import settings
import requests

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

def profil_view(request):
    return render(request, 'app/profil.html')

def redaktirovanie_view(request, telegram_id):
    student = get_object_or_404(Student, telegram_id=telegram_id)

    if request.method == 'POST':
        # Обновляем данные студента
        student.name = request.POST.get('name')
        student.birth_year = request.POST.get('birth_year')
        new_gender = request.POST.get('gender')  # Новый пол, выбранный пользователем
        student.campus = request.POST.get('campus')
        student.about_me = request.POST.get('about_me')

        # Обработка загрузки аватарки
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            file_name = default_storage.save(avatar.name, avatar)
            student.avatar = file_name
        else:
            # Если аватарка не загружена, проверяем, нужно ли обновить её на дефолтную
            if student.avatar in [settings.STATIC_URL + 'app/images/male.png', settings.STATIC_URL + 'app/images/female.png']:
                # Если текущая аватарка дефолтная, обновляем её в зависимости от нового пола
                if new_gender == 'male':
                    student.avatar = settings.STATIC_URL + 'app/images/male.png'
                else:
                    student.avatar = settings.STATIC_URL + 'app/images/female.png'

        # Обновляем пол студента
        student.gender = new_gender

        student.save()
        return redirect('profil', telegram_id=telegram_id)  # Перенаправляем на страницу профиля

    return render(request, 'app/redaktirovanie.html', {'student': student})

def startnoreg_view(request):
    return render(request, 'app/StartNoReg.html')

def yvedomlenia_view(request, telegram_id):
    # Получаем объект текущего студента
    current_student = get_object_or_404(Student, telegram_id=telegram_id)
    
    # Получаем все лайки, поставленные текущему студенту
    received_likes = Like.objects.filter(to_whow=telegram_id)
    
    # Получаем все лайки, поставленные текущим студентом
    given_likes = Like.objects.filter(from_whom=telegram_id)
    
    # Создаем список уведомлений
    notifications = []
    
    # Обрабатываем полученные лайки
    for like in received_likes:
        liked_by = Student.objects.get(telegram_id=like.from_whom)
        
        # Проверяем, есть ли взаимный лайк
        mutual_like = Like.objects.filter(
            from_whom=telegram_id,
            to_whow=like.from_whom
        ).exists()
        
        # Если у пользователя нет username, пытаемся получить его через Bot API
        if not liked_by.username:
            try:
                response = requests.get(
                    f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/getChat',
                    params={'chat_id': liked_by.telegram_id}
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('ok') and data.get('result', {}).get('username'):
                        liked_by.username = data['result']['username']
                        liked_by.save()
            except Exception as e:
                print(f"Error getting username for user {liked_by.telegram_id}: {e}")
        
        notifications.append({
            'student': liked_by,
            'mutual': mutual_like
        })
    
    return render(request, 'app/yvedomlenia.html', {
        'student': current_student,
        'notifications': notifications
    })

def znakomstva_view(request, telegram_id):
    # Получаем объект текущего студента
    current_student = get_object_or_404(Student, telegram_id=telegram_id)
    
    # Получаем всех студентов, кроме текущего
    students = Student.objects.exclude(telegram_id=telegram_id)
    
    # Передаем объекты в контекст шаблона
    context = {
        'student': current_student,
        'current_student': current_student,
        'students': students,
    }
    return render(request, 'app/znakomstva.html', context)

def profil_view(request, telegram_id):
    # Получаем объект студента по telegram_id
    student = get_object_or_404(Student, telegram_id=telegram_id)
    
    # Передаем объект студента в контекст шаблона
    context = {
        'student': student,
    }
    return render(request, 'app/profil.html', context)

def upload_avatar(request, telegram_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, telegram_id=telegram_id)
        if 'avatar' in request.FILES:
            student.avatar = request.FILES['avatar']
            student.save()
            messages.success(request, 'Аватарка успешно обновлена!')
        else:
            messages.error(request, 'Файл не выбран.')
    return redirect('success', telegram_id=telegram_id)

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
            about_me = request.data.get('about_me')
            # Создаем нового студента
            student = Student.objects.create(
                telegram_id=telegram_id,
                name=name,
                campus=campus,
                birth_year=birth_year,
                gender=gender,
                about_me=about_me,
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

def profile_detail_view(request, current_telegram_id, viewed_telegram_id):
    # Получаем объекты студентов
    current_student = get_object_or_404(Student, telegram_id=current_telegram_id)
    viewed_student = get_object_or_404(Student, telegram_id=viewed_telegram_id)
    
    # Проверяем, существует ли лайк
    existing_like = Like.objects.filter(
        from_whom=current_telegram_id,
        to_whow=viewed_telegram_id
    ).exists()
    
    context = {
        'current_student': current_student,
        'viewed_student': viewed_student,
        'existing_like': existing_like,
    }
    return render(request, 'app/profile_detail.html', context)

def like_profile_view(request, current_telegram_id, viewed_telegram_id):
    if request.method == 'POST':
        # Проверяем, существует ли уже такой лайк
        existing_like = Like.objects.filter(
            from_whom=current_telegram_id,
            to_whow=viewed_telegram_id
        ).first()
        
        if existing_like:
            # Если лайк существует, удаляем его
            existing_like.delete()
            messages.success(request, 'Вы убрали лайк!')
        else:
            # Создаем новый лайк
            Like.objects.create(
                from_whom=current_telegram_id,
                to_whow=viewed_telegram_id
            )
            messages.success(request, 'Вы поставили лайк!')
            
    return redirect('profile_detail', current_telegram_id=current_telegram_id, viewed_telegram_id=viewed_telegram_id)
