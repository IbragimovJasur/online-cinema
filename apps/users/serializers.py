from rest_framework import serializers
from apps.users.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields= ['first_name', 'last_name', 'username', 'email', 'avatar', 'tarrifs', 'interested_genres']
