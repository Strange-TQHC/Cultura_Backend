from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('protected/', views.protected_test),
    path('ai-description/', views.generate_description),
    path('places/', views.get_places),
    path('contributions/<int:place_id>/', views.get_contributions),
    path('find-place/', views.find_place),
    path('add-contribution/', views.add_contribution),
]