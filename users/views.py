from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .custom_permissions import IsOwnerOrAdmin
from .serializers import UserSerializer


class UserCreateView(generics.CreateAPIView):
    """
    Allowed Methods:
        POST: Create a new user
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserDeleteView(generics.DestroyAPIView):
    """
    Allowed Methods:
        DELETE: Delete a user if you're an admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdminUser,)

class UserUpdateView(generics.UpdateAPIView):
    """
    Allowed Methods: 
        PUT: Update a user if you're the user or an admin
        PATCH: Partially update a user if you're the user or an admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin,)