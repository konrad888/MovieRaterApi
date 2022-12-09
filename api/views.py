from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,) #AllowAny

    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                # update
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response_data = {'message': 'Rating updated!', 'data': serializer.data}
                response_status = status.HTTP_200_OK
            except:
                # new
                Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response_data = {'message': 'Rating created!', 'data': serializer.data}
                response_status = status.HTTP_200_OK
        else:
            response_data = {'message': 'You need to provide a star rating'}
            response_status = status.HTTP_400_BAD_REQUEST
        return Response(response_data, status=response_status)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        response_data = {'message': 'Not allowed!'}
        response_status = status.HTTP_405_METHOD_NOT_ALLOWED
        return Response(response_data, status=response_status)

    def create(self, request, *args, **kwargs):
        response_data = {'message': 'Not allowed!'}
        response_status = status.HTTP_405_METHOD_NOT_ALLOWED
        return Response(response_data, status=response_status)