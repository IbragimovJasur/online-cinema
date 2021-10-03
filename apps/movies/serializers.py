from rest_framework import serializers
from .models import Movie, Rating

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        exclude= ['uploaded_to_platform_in', 'uploaded_to_platform_by']

class RateMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rating
        fields= ['rate', 'opinion']
        