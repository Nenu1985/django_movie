from django import template
from movies.models import Category, Movie


register = template.Library()
'''
Template tags are used like mixins - to incluse extra logic into some class behaviour.

In this case we add the feature to display all the categories on the main page and on the detailed movie page.
To enable tags on the page we should add {% load movie_tag %} to the top of the template file ('header.html')
and in the template call the tag' name ('get_categories') which returns a list of Category
'''

# Registration template tag

@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()


# Inclusion tag can render a template (see movies/tags/last_movie.html)
@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}
