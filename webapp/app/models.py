from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from datetime import datetime

class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название интереса")

    class Meta:
        verbose_name = "Интерес"
        verbose_name_plural = "Интересы"

    def __str__(self):
        return self.name

class Like(models.Model):
    from_whom = models.CharField(max_length=200, verbose_name="like from")
    to_whow = models.CharField(max_length=200, verbose_name="like to")

    def __str__(self):
        return self.from_whom


class Student(models.Model):
    CAMPUS_CHOICES = [
        ('1', 'Корпус 1'),
        ('2', 'Корпус 2'),
        ('3', 'Корпус 3'),
        ('4', 'Корпус 4'),
    ]

    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    telegram_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=200, verbose_name="Имя")
    campus = models.CharField(max_length=1, choices=CAMPUS_CHOICES, verbose_name="Корпус")
    birth_year = models.IntegerField(
        verbose_name="Год рождения",
        validators=[
            MinValueValidator(1900),  # Минимальный год рождения
            MaxValueValidator(2024),  # Максимальный год рождения (текущий год)
        ]
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Пол")
    about_me = models.TextField(blank=True, verbose_name="О себе", default='Я студент Курского Государственного Политехнического Колледжа!')
    interests = models.ManyToManyField(Interest, blank=True, verbose_name="Интересы", related_name="students")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватарка")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Если аватарка не задана, выбираем её в зависимости от пола
        if not self.avatar:
            if self.gender == 'male':
                self.avatar = 'app/images/male.png'
            elif self.gender == 'female':
                self.avatar = 'app/images/female.png'
        super().save(*args, **kwargs)

    def avatar_preview(self):
        if self.avatar:
            return mark_safe(f'<img src="{self.avatar.url}" width="150" height="150" />')
        elif self.gender == 'male':
            return mark_safe('<img src="/static/app/images/male.png" width="150" height="150" />')
        elif self.gender == 'female':
            return mark_safe('<img src="/static/app/images/female.png" width="150" height="150" />')
        return "No Avatar"
    

    avatar_preview.short_description = 'Аватарка'
    avatar_preview.allow_tags = True