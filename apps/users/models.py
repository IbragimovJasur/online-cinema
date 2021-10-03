from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from apps.movies.models import Genre

class CustomUser(AbstractUser):

    TARRIF_CHOICHES= [
        ('Basic', '160 hours per month ($10)'),
        ('Standard', '200 hours per month ($15)'),
        ('Premium', 'unlimited hours per month ($25)'),
    ]
    first_name= models.CharField(
        "First Name", max_length=50, null= True, blank=True)
    last_name= models.CharField(
        "Last Name", max_length=50, null= True, blank=True)
    email= models.EmailField(
        "Email", unique=True, null=False, blank=False)
    avatar= models.ImageField(
        "Profile Picture", upload_to= "profile/avatars/", default= "profile/avatars/default.jpg")
    bill= models.DecimalField(
        "Bill of user", max_digits=6, decimal_places=2, default=0)
    tarrifs= models.CharField(
        "Tarrifs in the platform", max_length=50, choices=TARRIF_CHOICHES, null=False, blank=False)
    interested_genres= models.ManyToManyField(
        Genre, related_name='liked_genres', help_text='Press Ctrl to choose more than one', blank=True)

    objects= UserManager()
    REQUIRED_FIELDS = ['email', 'tarrifs']

    def __str__(self):
        return self.username
