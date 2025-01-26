from rest_framework import serializers
from .models import Product, Interaction, UserPreferences
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

CustomUser = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensures password is only writeable

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove the password from the validated data
        user = CustomUser(**validated_data)  # Create a new CustomUser instance

        # Hash the password before saving
        user.password = make_password(password)
        user.save()

        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'category', 'description', 'image', 'created_at', 'updated_at']


class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['user', 'product', 'interaction_type', 'interaction_count', 'created_at']


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['user', 'preferred_product_type', 'preferred_description', 'interaction_count', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(many=True)  # Include user preferences in the profile

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'preferences']  # Include other fields if needed
