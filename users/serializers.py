from djoser.serializers import UserCreateSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    role = serializers.ChoiceField(choices=User.ROLES, required=True, write_only=False)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')
        read_only_fields = ('id',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        if 'role' not in validated_data:
            raise serializers.ValidationError({'role': 'Ce champ est obligatoire.'})
        return super().create(validated_data)

class CustomUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'role')