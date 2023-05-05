from rest_framework import serializers
from .models import User

class User_basic_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'pw', 'email')