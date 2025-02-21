from rest_framework import generics
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student, Interest, Like
from urllib.parse import parse_qs
from .serializers import StudentSerializer, InterestSerializer, LikeSerializer
from django.shortcuts import render
import hmac
import hashlib
import json

#def index(request):
#    return render(request, 'app/fio.html')
def korpus_view(request):
    return render(request, 'app/korpus.html')

@csrf_exempt  # Отключаем CSRF-защиту для этого представления
def index(request):
    if request.method == 'POST':
        try:
            # Получаем initData из тела запроса
            data = json.loads(request.body)
            init_data = data.get('initData')
            
            if init_data:
                # Проверяем подлинность initData
                if validate_init_data(init_data, '7561904095:AAFmcA68_Y7vgOjiPnjXiKxUR28idE6_pCM'):
                    # Парсим initData для получения user_id
                    user_id = parse_init_data(init_data)
                    return JsonResponse({'user_id': user_id})
                else:
                    return JsonResponse({'error': 'Invalid initData'}, status=400)
            else:
                return JsonResponse({'error': 'initData not provided'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def parse_init_data(init_data):
    """
    Парсим initData для извлечения user_id.
    """
    parsed_data = parse_qs(init_data)
    user = parsed_data.get('user', [None])[0]
    if user:
        user_id = user.get('id')
        return user_id
    return None

def validate_init_data(init_data, bot_token):
    """
    Проверяет подлинность initData с использованием HMAC.
    """
    try:
        # Разделяем данные на пары ключ-значение
        pairs = init_data.split('&')
        data = {}
        for pair in pairs:
            key, value = pair.split('=')
            data[key] = value

        # Получаем хэш и данные
        received_hash = data.pop('hash')
        data_string = '\n'.join(f"{k}={v}" for k, v in sorted(data.items()))

        # Вычисляем HMAC
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        computed_hash = hmac.new(secret_key, data_string.encode(), hashlib.sha256).hexdigest()

        # Сравниваем хэши
        return hmac.compare_digest(computed_hash, received_hash)
    except Exception as e:
        print(f"Error validating initData: {e}")
        return False

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
