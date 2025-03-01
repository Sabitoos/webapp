# your_app_name/urls.py
from django.urls import path
from . import views
from .views import index, CheckIDView, reg_page, fio_page
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('interests/', views.InterestListCreate.as_view(), name='interest-list-create'),
    path('interests/<int:pk>/', views.InterestRetrieveUpdateDestroy.as_view(), name='interest-retrieve-update-destroy'),
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view(), name='student-retrieve-update-destroy'),
    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeRetrieveUpdateDestroy.as_view(), name='like-retrieve-update-destroy'),

    path('', index, name='index'),  # Главная страница
    path('checkid/', CheckIDView.as_view(), name='checkid'),  # Обработка telegram_id
    path('start/', reg_page, name='start'), # Отправка на регистрацию 
    path('fio/', fio_page, name='fio')
#    path('', views.index, name='index'),  # Маршрут для главной страницы
#    path('korpus.html', views.korpus_view, name='korpus'), 
    
]
