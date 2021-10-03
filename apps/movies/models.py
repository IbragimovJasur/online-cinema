import decimal
from django.db import models
from django.conf import settings


class Genre(models.Model):
    genre_name= models.CharField("Genre name", max_length=50, null=False, blank=False)

    def __str__(self):
        return self.genre_name


def get_img_upload_path(instance, filename):
    return f'films/{instance.name}/{filename}'

class Movie(models.Model):
    TYPE_CHOICES= [
        ('movie', 'Movie'),
        ('serial', 'Serial'),
    ]

    uploaded_to_platform_by= models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_movies', null=True, blank=True)
    genres= models.ManyToManyField(Genre, related_name='films', blank=False)
    name= models.CharField(
        "Name of Movie/Serial", max_length=150, unique=True, null=False, blank=False)
    was_shot_by= models.CharField(
        "Film was shot by whom or which studio",max_length=100, null=False, blank=False)
    released_in= models.DateField(
        "Film was released in", null=False, blank=False )
    duration= models.CharField(
        "Duration of film", max_length=100, null=False, blank=False)
    actors= models.CharField(
        "Actors who starred in the film", max_length=150, null=False, blank=False)
    description= models.TextField("Detailed information about film")
    video= models.FileField(
        "Video content of film", upload_to= get_img_upload_path, null=False, blank=False)
    type= models.CharField(
        "Type of film", choices=TYPE_CHOICES, max_length=50, null=False, blank=False)
    uploaded_to_platform_in= models.DateTimeField(auto_now_add=True)
    rating_of_film= models.FloatField(max_length=1, default=0.0)
    num_rated_users= models.IntegerField(default=0)

    def __str__(self):
        return self.name
        

class Rating(models.Model):
    VERY_BAD= 1
    BAD= 2
    SATISFIED= 3
    EXCELLENT= 4
    MASTERPIECE= 5

    RATING_CHOICES= [
        (VERY_BAD, 'Very Bad'),
        (BAD, 'Bad'),
        (SATISFIED, 'Satisfied'),
        (EXCELLENT, 'Excellent'),
        (MASTERPIECE, 'Masterpiece'),
    ]

    rated_by= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True)
    movie= models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rate= models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=False, blank=False)
    opinion= models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rated_by.username