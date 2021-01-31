from django.urls import path

from . import rest_views

urlpatterns = [
    path('movie', rest_views.MovieListView.as_view()),
    path('movie/<int:pk>', rest_views.MovieDetailView.as_view()),
    path('review/', rest_views.ReviewCreateView.as_view()),
]