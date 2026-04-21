from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import UserProfile, Place, Contribution
from .serializers import UserProfileSerializer, PlaceSerializer, ContributionSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
import requests

@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_test(request):
    return Response({
        "message": "You are authenticated",
        "user": request.user.username
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def generate_description(request):
    name = request.data.get('name')
    place_type = request.data.get('type')

    prompt = f"""
    Explain the cultural significance of a place named "{name}".
    It is a type of "{place_type}".
    Keep it short and simple for travelers.
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        result = data.get("response", "")

        return Response({"description": result})

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_places(request):
    places = Place.objects.all()
    serializer = PlaceSerializer(places, many=True)
    return Response(serializer.data)    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_contributions(request, place_id):
    contributions = Contribution.objects.filter(place_id=place_id)
    serializer = ContributionSerializer(contributions, many=True)
    return Response(serializer.data)