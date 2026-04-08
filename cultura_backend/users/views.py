from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Create Django user
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )

    # Create profile
    UserProfile.objects.create(
        user=user,
        name=request.data.get('name'),
        age=request.data.get('age'),
        gender=request.data.get('gender'),
        current_location=request.data.get('current_location'),
        permanent_location=request.data.get('permanent_location'),
        food_preferences=request.data.get('food_preferences'),
    )

    return Response({"message": "User created successfully"})

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(username=email, password=password)

    if user is None:
        return Response({"error": "Invalid credentials"}, status=400)

    token, _ = Token.objects.get_or_create(user=user)

    profile = user.userprofile

    return Response({
        "message": "Login successful",
        "token": token.key,
        "user_id": user.id,
        "name": profile.name,
        "permanent_location": profile.permanent_location
    })