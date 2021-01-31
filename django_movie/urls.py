"""django_movie URL Configuration
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('djadmin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/v1/', include('movies.rest_urls')),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('allauth.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),  # flat pages
    path('contact/', include("contact.urls")),
    path("", include("movies.urls")),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

