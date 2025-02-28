from rest_framework import generics
from .models import Student, Interest, Like
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render, redirect
from dotenv import load_dotenv
load_dotenv()
from django.http import HttpResponse

def index(request):
    return render(request, 'app/index.html')
#def korpus_view(request):
#    return render(request, 'app/korpus.html')

def checkid(request):
    if request.method == 'POST':
        telegramid = request.POST.get('telegramid')  # Получаем telegramid из формы
        if telegramid:
            if Student.objects.filter(telegramid=telegramid).exists():
                return HttpResponse('ID существует в базе данных')
            else:
                Student.objects.create(telegramid=telegramid)  # Создаем новую запись
                return HttpResponse('ID был занесен в базу данных')
        else:
            return HttpResponse('Ошибка: telegramid не указан', status=400)
    else:
        # Если метод не POST, возвращаем ошибку 405 (Method Not Allowed)
        return HttpResponse('Метод не разрешен', status=405)






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
