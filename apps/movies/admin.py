from django.contrib import admin
from .models import Genre, Movie, Rating

models_to_register= [Genre, Movie, Rating]

for one_model in models_to_register:
    admin.site.register(one_model)
    