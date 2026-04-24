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
from django.db.models import Q

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
    contributions = request.data.get('contributions', [])

    combined_text = " ".join([c['content'] for c in contributions])

    prompt = f"""
    You are a cultural guide.

    Place: {name}
    Type: {place_type}

    Local Information:
    {combined_text}

    Explain this place in a helpful and engaging way for travelers.
    Keep it short and meaningful.
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_place(request):
    name = request.GET.get('name', '')

    place = Place.objects.filter(
        Q(name__icontains=name)
    ).first()

    if place:
        return Response({
            "id": place.id,
            "name": place.name,
        })
    else:
        return Response({"id": None})
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_contribution(request):
    user = request.user
    place_id = request.data.get('place_id')
    category = request.data.get('category')
    content = request.data.get('content')

    try:
        place = Place.objects.get(id=place_id)
    except Place.DoesNotExist:
        return Response({"error": "Place not found"}, status=404)

    contribution = Contribution.objects.create(
        user=user,
        place=place,
        category=category,
        content=content
    )

    return Response({
        "message": "Contribution added successfully"
    })    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_contributions(request):
    contributions = Contribution.objects.filter(user=request.user)

    serializer = ContributionSerializer(contributions, many=True)
    return Response(serializer.data)