
import os
import cv2
import numpy as np
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Movie, Rating
from .models import User
from .serializers import MovieSerializer, RatingSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from PIL import Image
from keras.models import load_model
from rest_framework.parsers import MultiPartParser, FormParser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [AllowAny]

    @action(detail=False, methods=['patch'])
    def partial_update_email(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        model_path = 'modelDL/cnn_liveness_detection.h5'
        load_model1 = load_model(model_path)
        img_path = "images/user_face.png"
        img = cv2.imread(img_path)
        img = Image.open(img_path)
        # Adjust size based on your model requirements
        img = img.resize((224, 224))
        img = np.array(img) / 255.0
        img = img.reshape(1, 224, 224, 3)

        # Make predictions
        predictions = load_model1.predict(img)
        print(predictions)
        print(predictions[0][0])
        if predictions > 0.7:
            request.data['email'] = '1@gmail.com'
        else:
            request.data['email'] = '0@gmail.com'
        if serializer.is_valid():
            serializer.save()
            try:
                os.remove(img_path)
            except FileNotFoundError:
                print(f"Không tìm thấy {img_path}")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating updated', 'results': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(
                    user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {
                    'message': 'Rating created', 'results': serializer.data
                }
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'You need to provide stars'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UploadImageView(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
