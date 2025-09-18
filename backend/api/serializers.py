from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Search, RegistrationCode

class UserSerializer(serializers.ModelSerializer):
    registration_code = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'registration_code']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_registration_code(self, value):
        """Validate that the registration code exists and is valid"""
        try:
            code = RegistrationCode.objects.get(code=value)
            if not code.is_valid():
                if code.is_used:
                    raise serializers.ValidationError(
                        "This registration code has already been used."
                    )
                else:
                    raise serializers.ValidationError("This registration code has expired.")
            return value
        except RegistrationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid registration code.")

    def create(self, validated_data):
        # Extract and remove registration_code from validated_data
        registration_code = validated_data.pop('registration_code')

        # Create the user
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Mark the registration code as used
        code = RegistrationCode.objects.get(code=registration_code)
        code.use_code(user)

        return user

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['id', 'user', 'query', 'created_at']
        read_only_fields = ['id', 'created_at']
