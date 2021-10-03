from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveAPIView
from apps.users.models import CustomUser
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from apps.users.serializers import CustomUserSerializer
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
class CustomUserCreateView(CreateAPIView):
    permission_classes= [AllowAny]
    queryset= CustomUser.objects.all()
    serializer_class= CustomUserSerializer


class CustomUserUpdateView(RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated, IsProfileOwner]
    queryset= CustomUser.objects.all()
    serializer_class= CustomUserSerializer


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
            print(request.data)
            new_movie= Movie.objects.get(uploaded_to_platform_by= request.user)
            Rating.objects.create(movie= new_movie, rate=0) #adding film to rating model
            
            return Response(serializer.data, status= HTTP_200_OK)
        else:
            return Response(serializer.errors, status= HTTP_400_BAD_REQUEST)


class MovieRetrieveView(RetrieveAPIView):
    permission_classes= [IsAuthenticated]
    queryset= Movie.objects.all()
    serializer_class= MovieSerializer


class MovieUpdateDeleteView(APIView):
    permission_classes= [IsOwner]
    queryset= Movie.objects.all()
    serializers_class= MovieSerializer

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise HTTP_404_NOT_FOUND

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MovieSerializer(snippet)
        return Response(serializer.data, status= HTTP_200_OK)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = MovieSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
                old_rate= rating_info.rate / rating_info.num_rated_users 
                rating_info.rating_of_film -= old_rate   #substract old rate value of user from total rating of movie

                rate_to_add= serializer.data.get('rate') / rating_info.num_rated_users #divide rate by total number of rated users
                rating_info.rating_of_film += rate_to_add

                rating_info.save()
                return Response(serializer.data, status= HTTP_200_OK)
            
            except: #if user is rating film for the first time
                movie_going_tobe_rated= Rating.objects.get(movie= rated_movie)
                movie_going_tobe_rated.rated_by = request.user
                movie_going_tobe_rated.num_rated_users += 1
                rated_users= movie_going_tobe_rated.num_rated_users

                if rated_users == 0:
                    movie_going_tobe_rated.rating_of_film = serializer.data.get('rate')
                    movie_going_tobe_rated.save()
                else:
                    rate_to_add= serializer.data.get('rate') / rated_users #divide rate by total number of rated users
                    movie_going_tobe_rated.rating_of_film += rate_to_add
                    movie_going_tobe_rated.save()

                return Response(serializer.data, status= HTTP_200_OK)
