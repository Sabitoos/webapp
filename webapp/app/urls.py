# your_app_name/urls.py
from django.urls import path
from . import views
from .views import index, check_telegram_id
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('interests/', views.InterestListCreate.as_view(), name='interest-list-create'),
    path('interests/<int:pk>/', views.InterestRetrieveUpdateDestroy.as_view(), name='interest-retrieve-update-destroy'),
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view(), name='student-retrieve-update-destroy'),
    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeRetrieveUpdateDestroy.as_view(), name='like-retrieve-update-destroy'),

    path('', index, name='index'),  # Главная страница
    path('checkid/', check_telegram_id, name='checkid'),  # Обработка telegram_id

#    path('', views.index, name='index'),  # Маршрут для главной страницы
#    path('korpus.html', views.korpus_view, name='korpus'), 
    
]
