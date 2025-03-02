# your_app_name/urls.py
from django.urls import path
from . import views
from .views import index, CheckIDView, RegisterView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('interests/', views.InterestListCreate.as_view(), name='interest-list-create'),
    path('interests/<int:pk>/', views.InterestRetrieveUpdateDestroy.as_view(), name='interest-retrieve-update-destroy'),
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view(), name='student-retrieve-update-destroy'),
    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeRetrieveUpdateDestroy.as_view(), name='like-retrieve-update-destroy'),

    path('', index, name='index'),  # Главная страница
    path('checkid/', CheckIDView.as_view(), name='checkid'),  # Проверка Telegram ID
    path('register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('fio.html', views.fio_view, name='fio'),
    path('korpus.html', views.korpus_view, name='korpus'),
    path('god.html', views.god_view, name='god'),
    path('pol.html', views.pol_view, name='pol'),
    path('interes.html', views.interes_view, name='interes'),
    path('nastroika.html', views.nastroika_view, name='nastroika'),
    path('success/', views.success_view, name='success'),
    path('delete/', views.delete_account, name='delete_account'),  # Маршрут для success.html
]