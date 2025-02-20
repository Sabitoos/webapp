# your_app_name/urls.py
from django.urls import path
from . import views
from .views import check_telegram_id, register_student, home, logout

urlpatterns = [
    path('interests/', views.InterestListCreate.as_view(), name='interest-list-create'),
    path('interests/<int:pk>/', views.InterestRetrieveUpdateDestroy.as_view(), name='interest-retrieve-update-destroy'),
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view(), name='student-retrieve-update-destroy'),
    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeRetrieveUpdateDestroy.as_view(), name='like-retrieve-update-destroy'),
#    path('', views.index, name='index'),  # Маршрут для главной страницы
#    path('korpus.html', views.korpus_view, name='korpus'), 

    path('', check_telegram_id, name='check_telegram_id'),  # Корневой URL
    path('check-telegram-id/', check_telegram_id, name='check_telegram_id'),
    path('register/', register_student, name='register'),
    path('home/', home, name='home'),  # Главная страница
    path('logout/', logout, name='logout'),  # Выход
]
