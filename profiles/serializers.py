from rest_framework import serializers
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail

User = get_user_model()

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not check_password(value, user.password):
            raise serializers.ValidationError("old password is incorrect")
        return value
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        if len(data['new_password']) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})
        return data
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','bio','pronouns','phone_number']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','bio','pronouns','phone_number']