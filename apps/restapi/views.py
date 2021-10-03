from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from apps.users.models import CustomUser
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from apps.users.serializers import CustomUserRegistrationSerializer
from apps.movies.models import Movie, Rating
from apps.movies.serializers import MovieSerializer, RateMovieSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


#built permission classes
class IsProfileOwner(BasePermission):
      def has_object_permission(self, request, view, obj):
        return request.user == CustomUser.objects.get(pk=view.kwargs['pk'])

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        selected_movie= Movie.objects.get(pk= view.kwargs['pk']) 
        return request.user == selected_movie.uploaded_to_platform_by

#users
class CustomUserRegistrationView(CreateAPIView):
    permission_classes= [AllowAny] 
    queryset= CustomUser.objects.all()
    serializer_class= CustomUserRegistrationSerializer
    

class CustomUserUpdateView(RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated, IsOwner]
    queryset= CustomUser.objects.all()
    serializer_class= CustomUserRegistrationSerializer


#movie
class MovieListCreateView(ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset= Movie.objects.all()
    serializer_class= MovieSerializer
    parser_classes= [MultiPartParser, FormParser]

    def post(self, request, format=None):
        serializer= MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(uploaded_to_platform_by=self.request.user)            
            return Response(serializer.data, status= HTTP_200_OK)
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


class MovieRetrieveView(RetrieveAPIView):
    permission_classes= [IsAuthenticated]
    queryset= Movie.objects.all()
    serializer_class= MovieSerializer


class MovieUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes= [IsOwner]
    queryset= Movie.objects.all()
    serializer_class= MovieSerializer

class RateMovieCreateView(CreateAPIView):
    permission_classes= [IsAuthenticated]
    queryset= Rating.objects.all()
    serializer_class= RateMovieSerializer

    def post(self, request, *args, **kwargs):
        serializer= RateMovieSerializer(data= request.data)
        pk= self.kwargs['pk']
        rated_movie= Movie.objects.get(id= pk)

        if serializer.is_valid():
            try: #if user already rated the film
                rating_info= request.user.reviews.get(movie= rated_movie)   #search movie from user's rated films
                old_total= round(rated_movie.rating_of_film * rated_movie.num_rated_users, 1)
                old_total_without_users_rate= old_total - rating_info.rate
                new_total= old_total_without_users_rate + serializer.data.get('rate')
                rated_movie.rating_of_film= round(new_total / rated_movie.num_rated_users, 1)
                rated_movie.save()
                
                #update rate and opinion about that film
                rating_info.rate= serializer.data.get('rate')
                rating_info.opinion= serializer.data.get('opinion')
                rating_info.save()
                
                return Response(serializer.data, status= HTTP_200_OK)
            
            except: #if user is rating film for the first time
                new_rated_movie= Rating.objects.create(
                    rated_by= request.user,
                    movie= rated_movie,
                    rate= serializer.data.get('rate'),
                    opinion= serializer.data.get('opinion')
                )
                new_rated_movie.save()
                
                if rated_movie.num_rated_users == 0:
                    rated_movie.rating_of_film = serializer.data.get('rate')
                    rated_movie.num_rated_users += 1

                else:
                    total_rates= round(rated_movie.rating_of_film * rated_movie.num_rated_users, 1)
                    total_rates += serializer.data.get('rate')
                    rated_movie.num_rated_users += 1
                    rated_movie.rating_of_film= round(total_rates / rated_movie.num_rated_users, 1) 

                rated_movie.save()
                return Response(serializer.data, status= HTTP_200_OK)
