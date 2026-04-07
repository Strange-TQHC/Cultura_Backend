from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)

    current_location = models.CharField(max_length=255)
    permanent_location = models.CharField(max_length=255)

    food_preferences = models.TextField()

    def __str__(self):
        return self.email