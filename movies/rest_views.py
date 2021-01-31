
from django.db import models
from django.views import generic
from rest_framework.response import Response
from rest_framework import generics

from rest_framework.views import APIView

from .models import Actor, Movie
from .serializers import (
    CreateRatingSerializer,
    MovieListSerializer,
    MovieDetailSerializer,
    ReivewCreateSerializer,
    ActorListSerializer,
)
from .service import get_client_ip
class MovieListView(APIView):
    ''' Movie list '''
    def get(self, request):
        # 1 way: Adding extra field rating_user to check if movie has a rating;
        # Disadvantage of this aproach is that each movie would be appear as many times as ratings have been made by each user;
        # movies = Movie.objects.filter(draft=False).annotate(
        #     rating_user=models.Case(  # Case is similar to if..elif...else
        #         models.When(ratings__ip=get_client_ip(request), then=True),  # ratings__ip - calling ip field from the related retings 
        #         default=False,
        #         output_field=models.BooleanField()
        #     ),
        # )
        # Second way:
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
            ).annotate(
           middle_star=models.Sum(models.F('ratings__star')) * 1.0 / models.Count(models.F('ratings'))  # F - для выполнения математ операций
        )

        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    ''' Movie list '''
    def get(self, request, pk):
        movies = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movies)  # many=False (because only one record)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    ''' Movie list '''
    def post(self, request):
        review = ReivewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStartRatingView(APIView):
    ''' Adding movie's rate '''

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request=request))
            return Response(status=201)
        else:
            return Response(status=400)


# Generic ListAPiView - useful class to impelement get/post just pointing out queryset and serializer
class ActorListView(generics.ListAPIView):
    ''' List of actors'''
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer
