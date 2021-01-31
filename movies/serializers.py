from rest_framework import serializers

from .models import Movie, Reviews


class MovieListSerializer(serializers.ModelSerializer):
    ''' Movie list '''
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category')


class ReivewCreateSerializer(serializers.ModelSerializer):
    ''' Adding review '''
    class Meta:
        model = Reviews
        fields = '__all__'  # all fields to display


class ReivewSerializer(serializers.ModelSerializer):
    ''' Adding review '''
    class Meta:
        model = Reviews
        fields = ('name', 'text', 'parent')

class MovieDetailSerializer(serializers.ModelSerializer):
    ''' Movie details '''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)  # To display category name instead of id
    directors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)

    reviews = ReivewSerializer(many=True)
    class Meta:
        model = Movie
        exclude = ('draft', )  # all field except 'draft'


