from django.contrib import admin
from .models import UserProfile, Place, Contribution

admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Contribution)