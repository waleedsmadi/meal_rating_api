from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Meal, Rating, Favorite
from .serializers import MealSerializer, RatingSerializer, FavoriteSerializer, UserSerializer
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)
    

    def list(self, request, *args, **kwargs):
        return Response({'message': 'You can not list users by this way!'}, status=status.HTTP_400_BAD_REQUEST)



    def retrieve(self, request, *args, **kwargs):
        return Response({'message': 'You can not get a user by this way!'}, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):
        return Response({'message': 'You can not delete a user by this way!'}, status=status.HTTP_400_BAD_REQUEST)


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        user = request.user
        stars = request.POST.get('stars')

        if not stars:
            return Response({'error': 'stars field is required!'}, status=status.HTTP_400_BAD_REQUEST)
        


        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response({'error': 'this meal does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        

        try:
            stars = int(stars)
            if stars < 1 or stars > 5:
                raise ValueError
        except ValueError:
            return Response({'error': 'stars must be an integer between 1 and 5!'}, status=status.HTTP_400_BAD_REQUEST)
        

        if Rating.objects.filter(user=user, meal=meal).exists():
            rating = Rating.objects.get(user=user, meal=meal)
            rating.stars = stars
            rating.save()
            serializer = RatingSerializer(rating)
            return Response({'message': 'this meal rating has been updated!', 'result': serializer.data}, status=status.HTTP_200_OK)

            
        else:
            rating = Rating.objects.create(user=user, meal=meal, stars=stars)
            serializer = RatingSerializer(rating)
            return Response({'message': 'this meal rating has been created!', 'result': serializer.data}, status=status.HTTP_201_CREATED)


    @action(methods=['POST'], detail=True)
    def favorite_meal(self, request, pk=None):
        user = request.user

        try:
            meal = Meal.objects.get(pk=pk)
        except Meal.DoesNotExist:
            return Response({'error': 'this meal does not exist!'}, status=status.HTTP_404_NOT_FOUND)
        
        
        fav, created = Favorite.objects.get_or_create(user=user, meal=meal)
        if created:
            serializer = FavoriteSerializer(fav)
            return Response({'message': 'this meal is in favorite list now!', 'result': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            fav.delete()
            return Response({'message': 'this meal has been deletd from favorite list'}, status=status.HTTP_204_NO_CONTENT)



    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return (AllowAny(),)
        return (IsAuthenticated(),)

class RatingViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer



class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer