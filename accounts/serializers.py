from rest_framework import serializers
from django.core.mail import send_mail
from decouple import config
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','email','password']
        extra_kwargs = {"password":{
            "write_only":True
        }}

    def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
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

            return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField() 
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()

        if not user:
            raise serializers.ValidationError("user not found!")
        if not user.is_active:
            raise serializers.ValidationError("email not verified")
        if not user.check_password(data['password']):
            raise serializers.ValidationError("incorrect password")
        
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
     email = serializers.EmailField()

     def validate_email(self, value):
          if not User.objects.filter(email=value).exists():
               raise serializers.ValidationError("no account with this email found")
          return value
     
     def save(self):
          email = self.validated_data['email']
          user = User.objects.get(email=email)

          token = RefreshToken.for_user(user).access_token
          reset_link = f"http://localhost:8000/api/accounts/reset-password-confirm/?token={str(token)}"

          send_mail(
               "Reset Your Password",
               f"Click the link to reset your password: {reset_link}",
               config('EMAIL_HOST_USER'),
               [user.email],
               fail_silently=False
          )

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            access_token = AccessToken(data['token'])
            self.user_id = access_token['user_id']
        except Exception:
            raise serializers.ValidationError("Invalid or expired token.")
        return data

    def save(self):
        user = User.objects.get(id=self.user_id)
        user.set_password(self.validated_data['new_password'])
        user.save()
