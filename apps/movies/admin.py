from django.contrib import admin
from .models import Genre, Movie, Rating

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display= ['name', 'duration', 'type', 'rating_of_film', ]
    list_display_links= ['name']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display= ['rated_by', 'movie']
    list_display_links= ['rated_by']

admin.site.register(Genre)
    