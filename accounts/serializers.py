from rest_framework import serializers
from django.core.mail import send_mail
from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name','last_name','username','email','password']
        extra_kwargs = {"password":{
            "write_only":True
        }}

    def create(self, validated_data):
            user = CustomUser.objects.create_user(**validated_data)
            user.is_active = False
            user.save()

            token = RefreshToken.for_user(user).access_token
            verification_link = f"http://localhost:8000/api/accounts/verify-email/?token={str(token)}"

            send_mail(
                "Verify your Email",
                f"Click the link to verify your email: {verification_link}",
                config('EMAIL_HOST_USER'),
                [user.email],
                fail_silently=False
            )

            print(f"Verification email sent to: {user.email}")  # Debugging
            print(f"Verification link: {verification_link}")  # Debugging

            return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(email=data['email']).first()

        if not user:
            raise serializers.ValidationError("user not found!")
        if not user.is_active:
            raise serializers.ValidationError("email not verified")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("incorrect password")
        
        return user

