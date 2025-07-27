from django.contrib import admin
from .models import Meal, Rating



@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    search_fields = ['name', 'description']



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'meal', 'user']
    list_filter = ['user', 'meal']
    search_fields = ['user', 'meal']
