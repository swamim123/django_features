from abc import ABC

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UserLoginserializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


from rest_framework import serializers


class TokenRequestSerializer(serializers.Serializer):
    grant_type = serializers.CharField(required=True, initial='password')
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    client_id = serializers.CharField(required=True)
    client_secret = serializers.CharField(required=True)
