from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth.models import User
from .models import Song

class SongsSerializer(ModelSerializer):
    class Meta:
        model = Song
        fields = ("id","title", "artist")

class TokenSerializer(Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")