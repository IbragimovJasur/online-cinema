from django.urls import path
from .views import (
    CustomUserRegistrationView, 
    CustomUserUpdateView, 
    MovieListCreateView,
    MovieRetrieveView, 
    MovieUpdateDeleteView, 
    RateMovieCreateView
)

from rest_framework_swagger.views import get_swagger_view


schema_view= get_swagger_view(title='API Swagger')

urlpatterns= [
    #swagger
    path('swagger/', schema_view),
    
    #users
    path('user/register/', CustomUserRegistrationView.as_view(), name='custom_user_create'),
    path('user/update/<int:pk>/', CustomUserUpdateView.as_view(), name='custom_user_update'),

    #movies
    path('movie/', MovieListCreateView.as_view(), name='movie_list'),
    path('movie/detail/<int:pk>/', MovieRetrieveView.as_view(), name='movie_detail'),
    path('movie/detail/<int:pk>/updatedelete/', MovieUpdateDeleteView.as_view(), name='movie_updatedelete'),
    path('movie/detail/<int:pk>/rate/', RateMovieCreateView.as_view(), name='movie_rate'),
]
