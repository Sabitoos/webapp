# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from .models import Student, Interest

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.interest, created = Interest.objects.get_or_create(name="Programming")

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'telegram_id': '12345',
            'name': 'Test User',
            'campus': '1',
            'birth_year': '2000',
            'gender': 'male',
            'about_me': 'Test about me',
            'interests': [self.interest.id],
        })
        
        # Проверяем, что пользователь создан
        self.assertEqual(Student.objects.count(), 1)
        student = Student.objects.first()
        self.assertEqual(student.telegram_id, '12345')
        self.assertEqual(student.interests.count(), 1)