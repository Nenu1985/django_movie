
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializer, MovieDetailSerializer, ReivewCreateSerializer


class MovieListView(APIView):
    ''' Movie list '''
    def get(self, request):
        movies = Movie.objects.filter(draft=False)  # no drafts
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