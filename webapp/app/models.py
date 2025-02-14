from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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


    telegram_id = models.CharField(max_length=200, unique=True, verbose_name="Telegram ID")
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
    about_me = models.TextField(blank=True, verbose_name="О себе")
    interests = models.ManyToManyField(Interest, blank=True, verbose_name="Интересы", related_name="students")

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"

    def __str__(self):
        return self.name
