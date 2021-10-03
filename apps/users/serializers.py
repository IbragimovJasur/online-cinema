from rest_framework import serializers
from apps.users.models import CustomUser
from django.contrib.auth import authenticate

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        extra_kwargs = {'password': {'write_only': True}}
        fields= ['first_name', 'last_name', 'username', 'email', 'avatar', 'tarrifs', 'interested_genres', 'password', ]

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
