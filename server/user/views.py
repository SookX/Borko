from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from dotenv import load_dotenv
import os

# Create your views here.
@api_view(['POST'])
def register(request):
    
    """
    Registers a new user with the provided email, username, and password.
    And create dashboard related to the user.

    Args:
    - request (Request): The incoming HTTP request containing user registration data.

    Returns:
    - Response: A JSON response indicating success or failure of the registration process.
    """
    
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirmPassword')

    

    
    if not email or not username or not password:
        return Response({'error': 'Email, username, and password are required fields.'}, status=status.HTTP_400_BAD_REQUEST)

    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'An account with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    if password != confirm_password:
        return Response({'error': 'The passwords doesnt match!'}, status=status.HTTP_400_BAD_REQUEST)

    print("Booo")
    user = CustomUser(email=email, username=username, password=make_password(password))
    user.save()


    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login(request):

    """
    Authenticates a user with the provided email and password.

    Args:
    - request (Request): The incoming HTTP request containing user login credentials.

    Returns:
    - Response: A JSON response containing access and refresh tokens if authentication is successful, or an error message.
    """

    email = request.data.get('email')
    password = request.data.get('password')


    if not email or not password:
        return Response({'error': 'Email and password are required fields.'}, status=status.HTTP_400_BAD_REQUEST)


    user = authenticate(email=email, password=password)
    if user is None:
        return Response({'error': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)

