# your_app_name/urls.py
from django.urls import path
from . import views
from .views import index, CheckIDView, RegisterView, upload_avatar, delete_like
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('interests/', views.InterestListCreate.as_view(), name='interest-list-create'),
    path('interests/<int:pk>/', views.InterestRetrieveUpdateDestroy.as_view(), name='interest-retrieve-update-destroy'),
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentRetrieveUpdateDestroy.as_view(), name='student-retrieve-update-destroy'),
    path('likes/', views.LikeListCreate.as_view(), name='like-list-create'),
    path('likes/<int:pk>/', views.LikeRetrieveUpdateDestroy.as_view(), name='like-retrieve-update-destroy'),
    path('upload_avatar/<str:telegram_id>/', upload_avatar, name='upload_avatar'),

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
    path('delete/', views.delete_account, name='delete_account'),
    path('profil/<str:telegram_id>/', views.profil_view, name='profil'),
    path('edit/<str:telegram_id>/', views.redaktirovanie_view, name='edit'),
    path('notice/<str:telegram_id>/', views.yvedomlenia_view, name='notice'),
    path('znakomstva/<str:telegram_id>/', views.znakomstva_view, name='znakomstva'),
    path('profile/<int:current_telegram_id>/<int:viewed_telegram_id>/', views.profile_detail_view, name='profile_detail'),
    path('profile/<int:current_telegram_id>/<int:viewed_telegram_id>/like/', views.like_profile_view, name='like_profile'),
    path('interesred/<int:telegram_id>/', views.interesred_view, name='interesred'),
    path('delete_like/<str:from_whom>/<str:to_whow>/', delete_like, name='delete_like'),

    
]