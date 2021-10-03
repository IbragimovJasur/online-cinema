from django.contrib import admin
from .models import Genre, Movie, Rating

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display= ['name', 'duration', 'type']
    list_display_links= ['name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display= ['movie', 'rating_of_film', ]
    list_display_links= ['movie']

admin.site.register(Genre)
    