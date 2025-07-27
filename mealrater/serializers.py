from rest_framework import serializers
from .models import Meal, Rating, Favorite
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password




class MealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meal
        fields = ['pk', 'name', 'description']




class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['pk', 'meal', 'user', 'stars']




class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['pk', 'user', 'meal']



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['pk', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}
    

    def create(self, validated_data):
        user = User(**validated_data)
        user.password = make_password(validated_data['password'])
        user.save()
        return user
