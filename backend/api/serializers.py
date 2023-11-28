from .models import UserProfile
from rest_framework import serializers
from .models import Movie, Rating
from .models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname',
                  'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}, 'required': True}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        # Add your custom logic for updating user instance here
        return super().update(instance, validated_data)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'description',
                  'trailerLink', 'no_of_ratings', 'avg_rating')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'stars', 'user', 'movie')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('profile_image',)
