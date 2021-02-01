
from django.db import models
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Actor, Movie
from .serializers import (
    CreateRatingSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReivewCreateSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
)
from .service import get_client_ip, MovieFilter

# General APIView case:
# class MovieListView(APIView):
#     ''' Movie list '''
#     def get(self, request):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
#             ).annotate(
#            middle_star=models.Sum(models.F('ratings__star')) * 1.0 / models.Count(models.F('ratings'))  # F - для выполнения математ операций
#         )

#         serializer = MovieListSerializer(movies, many=True)
#         return Response(serializer.data)


# Generic API class usage:
class MovieListView(generics.ListAPIView):
    ''' Movie list '''
    serializer_class = MovieListSerializer
    # Connect to the class DjangoFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', 
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) * 1.0 / models.Count(models.F('ratings'))  # F - для выполнения математ операций
        )
        return movies


# class MovieDetailView(APIView):
#     ''' Movie list '''
#     def get(self, request, pk):
#         movies = Movie.objects.get(id=pk, draft=False)
#         serializer = MovieDetailSerializer(movies)  # many=False (because only one record)
#         return Response(serializer.data)

class MovieDetailView(generics.RetrieveAPIView):
    ''' Movie list '''
    serializer_class = MovieDetailSerializer
    # we don't need to use pk. RetrieveAPIView searchs required movie by primary key by itself
    queryset = Movie.objects.filter(draft=False)



# class ReviewCreateView(APIView):
#     ''' Movie list '''
#     def post(self, request):
#         review = ReivewCreateSerializer(data=request.data)
#         if review.is_valid():
#             review.save()
#         return Response(status=201)

class ReviewCreateView(generics.CreateAPIView):
    ''' Movie list '''
    serializer_class = ReivewCreateSerializer

# class AddStartRatingView(APIView):
#     ''' Adding movie's rate '''

#     def post(self, request):
#         serializer = CreateRatingSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(ip=get_client_ip(request=request))
#             return Response(status=201)
#         else:
#             return Response(status=400)

class AddStartRatingView(generics.CreateAPIView):
    ''' Adding movie's rate '''
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        ''' Send nesessary data we want to add to create an object '''
        serializer.save(ip=get_client_ip(self.request))

# Generic ListAPiView - useful class to impelement get/post just pointing out queryset and serializer
class ActorListView(generics.ListAPIView):
    ''' Returns List of actors'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorDetailView(generics.RetrieveAPIView):
    ''' Returns detail info about actor'''
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

