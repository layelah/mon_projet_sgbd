from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import CustomUserCreateSerializer

User = get_user_model()


class CustomUserCreateView(generics.CreateAPIView):
    model = User
    serializer_class = CustomUserCreateSerializer

    def create(self, request, *args, **kwargs):
        if 'role' not in request.data:
            return Response(
                {"role": ["Ce champ est obligatoire."]},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)