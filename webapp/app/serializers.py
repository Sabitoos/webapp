# your_app_name/serializers.py
from rest_framework import serializers
from .models import Student, Interest, Like

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    interests = InterestSerializer(many=True, read_only=True)  # Для отображения информации об интересах
    class Meta:
        model = Student
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def validate(self, data):
        """
        Проверка, что from_whom и to_whow не совпадают.
        """
        if data['from_whom'] == data['to_whow']:
            raise serializers.ValidationError("from_whom и to_whow не могут быть одинаковыми.")
        return data

