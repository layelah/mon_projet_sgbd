from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class CustomUserCreateSerializer(UserCreateSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, required=True)  # Ajouté ici

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')

    def validate_role(self, value):
        if value not in dict(User.ROLES):
            raise serializers.ValidationError("Rôle invalide. Choisissez 'teacher' ou 'student'.")
        return value

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'role')