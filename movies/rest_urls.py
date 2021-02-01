from django.urls import path
from django.urls.conf import include

from . import rest_views

urlpatterns = [
    path('movie', rest_views.MovieListView.as_view()),
    path('movie/<int:pk>', rest_views.MovieDetailView.as_view()),
    path('review/', rest_views.ReviewCreateView.as_view()),
    path('rating/', rest_views.AddStartRatingView.as_view()),
    path('actors/', rest_views.ActorListView.as_view()),
    path('actors/<int:pk>/', rest_views.ActorDetailView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),  # uing djoser auth token
    # path('auth/', include('djoser.urls.jwt')),  # using jwt auth token
]
