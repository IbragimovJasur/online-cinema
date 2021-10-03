from django.db import models

class Genre(models.Model):
    genre_name= models.CharField("Genre name", max_length=50, null=False, blank=False)

    def __str__(self):
        return self.genre_name
