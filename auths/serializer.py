from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import CustomUser as User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['password'] != attrs['re_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})


        try:
            user = User.objects.get(email=attrs['email'])
            if user:
                raise serializers.ValidationError({"email": "Email already exists."})
        except User.DoesNotExist:
            pass

        return attrs

    def create(self, validated_data):
        validated_data.pop('re_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
