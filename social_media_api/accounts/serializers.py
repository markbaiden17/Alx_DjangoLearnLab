from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        # Using get_user_model().objects.create_user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        
        # Manually handle bio if it's in the validated_data
        if 'bio' in validated_data:
            user.bio = validated_data['bio']
            user.save()
            
        Token.objects.create(user=user)
        return user