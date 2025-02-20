from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Interest

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.interest, created = Interest.objects.get_or_create(name="Programming")

    def test_registration(self):
        # Данные для регистрации
        data = {
            'telegram_id': '12345',
            'name': 'Test User',
            'campus': '1',
            'birth_year': '2000',
            'gender': 'male',
            'about_me': 'Test about me',
            'interests': [self.interest.id],
        }

        # Отправляем POST-запрос
        response = self.client.post(reverse('register'), data)
        
        # Проверяем, что запрос завершился успешно
        self.assertEqual(response.status_code, 302)  # 302 — перенаправление

        # Проверяем, что студент создан
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.telegram_id, '12345')
        self.assertEqual(student.name, 'Test User')
        self.assertEqual(student.interests.count(), 1)