import django_filters
from django_filters.rest_framework import filters

from .models import Movie


def get_client_ip(request):
    ''' Getting users' IP '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class MovieFilter(django_filters.rest_framework.FilterSet):
    # Genres is a many-to-many relation type. By default it search by id. To search by name
    # we should use CharFilterInFilter with lookup_exp='in'. The name genres searh is defined by
    # field_name
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    # searching by range
    year = django_filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'year']
