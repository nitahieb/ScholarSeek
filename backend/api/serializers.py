from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Search

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'registration_code']
        extra_kwargs = {'password': {'write_only': True}}
    registration_code = serializers.CharField(write_only=True)

    def validate_registration_code(self, value):
        if value != "Register123":
            raise serializers.ValidationError("Invalid registration code.")
        return value

    def create(self, validated_data):
        validated_data.pop('registration_code', None)
        user = User(
            email=validated_data.get('email', ''),
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['id', 'user', 'query', 'created_at']
        read_only_fields = ['id', 'created_at']
