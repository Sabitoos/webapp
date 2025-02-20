# your_app_name/views.py
from rest_framework import generics
from .models import Student, Interest, Like
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'app/fio.html')
def korpus_view(request):
    return render(request, 'app/korpus.html')

def home(request):
    # Проверяем, авторизован ли пользователь
    if 'telegram_id' in request.session:  # Используем сессию для хранения telegram_id
        try:
            # Получаем данные пользователя из базы данных
            student = Student.objects.get(telegram_id=request.session['telegram_id'])
            return render(request, 'app/home.html', {'student': student})
        except Student.DoesNotExist:
            # Если пользователь не найден, перенаправляем на страницу проверки telegram_id
            return redirect('check_telegram_id')
    else:
        # Если пользователь не авторизован, перенаправляем на страницу проверки telegram_id
        return redirect('check_telegram_id')
    
def logout(request):
    # Очищаем сессию
    if 'telegram_id' in request.session:
        del request.session['telegram_id']
    # Перенаправляем на страницу проверки telegram_id
    return redirect('check_telegram_id')

def check_telegram_id(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        
        try:
            student = Student.objects.get(telegram_id=telegram_id)
            # Сохраняем telegram_id в сессии
            request.session['telegram_id'] = telegram_id
            return redirect('home')
        except Student.DoesNotExist:
            return render(request, 'app/register.html', {'telegram_id': telegram_id})
    
    return render(request, 'app/check_telegram_id.html')

def register_student(request):
    if request.method == 'POST':
        telegram_id = request.POST.get('telegram_id')
        name = request.POST.get('name')
        campus = request.POST.get('campus')
        birth_year = request.POST.get('birth_year')
        gender = request.POST.get('gender')
        about_me = request.POST.get('about_me')
        
        # Создаем нового пользователя
        student = Student.objects.create(
            telegram_id=telegram_id,
            name=name,
            campus=campus,
            birth_year=birth_year,
            gender=gender,
            about_me=about_me,
        )
        
        # Сохраняем telegram_id в сессии
        request.session['telegram_id'] = telegram_id
        
        # Перенаправляем на главную страницу
        return redirect('home')
    
    return render(request, 'app/register.html')

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
