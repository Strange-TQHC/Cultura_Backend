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
    
class Place(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    place_type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('history', 'History'),
        ('folklore', 'Folklore'),
        ('etiquette', 'Etiquette'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.place.name} - {self.category}"    