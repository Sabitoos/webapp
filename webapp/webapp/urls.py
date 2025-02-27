# your_project/urls.py
from django.urls import path, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('app.urls')), # Включаем URL-адреса вашего приложения
    path('api-auth/', include('rest_framework.urls')), # Для аутентификации через API (опционально)

    path('', include('bot.urls')),
]
