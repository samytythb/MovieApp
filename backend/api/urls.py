from django.contrib import admin
from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, RatingViewSet, UserViewSet, UploadImageView


router = routers.DefaultRouter()
router.register('movies', MovieViewSet)
router.register('users', UserViewSet)
router.register('ratings', RatingViewSet)
router.register('uploads', UploadImageView)


urlpatterns = [
    path('', include(router.urls)),
]
