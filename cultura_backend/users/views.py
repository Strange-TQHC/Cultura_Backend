from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password

@api_view(['POST'])
def signup(request):
    data = request.data.copy()
    data['password'] = make_password(data['password'])
    
    serializer = UserSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"})

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    if not check_password(password, user.password):
        return Response({"error": "Invalid password"}, status=400)

    return Response({
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "permanent_location": user.permanent_location
    })