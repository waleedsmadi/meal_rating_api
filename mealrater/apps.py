from django.apps import AppConfig


class MealraterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mealrater'

    def ready(self):
        from .signals import token_created