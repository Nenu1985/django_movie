
from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Movie
from .serializers import CreateRatingSerializer, MovieListSerializer, MovieDetailSerializer, ReivewCreateSerializer


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


class AddStartRatingView(APIView):
    ''' Adding movie's rate '''
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request=request))
            return Response(status=201)
        else:
            return Response(status=400)