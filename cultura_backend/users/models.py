from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)

    current_location = models.CharField(max_length=255)
    permanent_location = models.CharField(max_length=255)

    food_preferences = models.TextField()

    def __str__(self):
        return self.user.email