from django.contrib import admin
from .models import LocationKnowledge, UserProfile, Place, Contribution

admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Contribution)
admin.site.register(LocationKnowledge)
