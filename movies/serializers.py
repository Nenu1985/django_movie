from rest_framework import serializers

from .models import Movie, Rating, Reviews


class MovieListSerializer(serializers.ModelSerializer):
    ''' Movie list '''
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)  # To display category name instead of id
    rating_user = serializers.IntegerField()
    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'rating_user')


class FilterReviewListSerializer(serializers.ListSerializer):
    ''' Review filtering
    Without this filtering all the reviews which hav parents are presenated both in parents (as nested)
    and individually.
    We need to leave single reviews (parent=None). Other reviews will be included to their parents.
    '''

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class ReivewCreateSerializer(serializers.ModelSerializer):
    ''' Adding review '''
    class Meta:
        model = Reviews
        fields = '__all__'  # all fields to display


class RecursiveSerializer(serializers.Serializer):
    ''' Display children recursevly '''

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReivewSerializer(serializers.ModelSerializer):
    ''' Display Review info '''
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer  # see FilterReviewListSerializer
        model = Reviews
        fields = ('name', 'text', 'parent', 'children')


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


class CreateRatingSerializer(serializers.ModelSerializer):
    ''' Adding user's rating to the movie '''
    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, created = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={
                'star': validated_data.get('star')
            }
        )
        return rating
        # return super().create(validated_data)