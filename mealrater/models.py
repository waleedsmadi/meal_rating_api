from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()


    def __str__(self):
        return self.name


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


    class Meta:
        constraints = [
            models.UniqueConstraint(name='uq_ratings_meal_user', fields=['meal', 'user']),
        ]
    

    def __str__(self):
        return self.user.username


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(name='uq_favorite_user_meal', fields=['user', 'meal']),
        ]

    def __str__(self):
        return f'{self.user.username} favorite -> {self.meal.name}'
