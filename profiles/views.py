from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from decouple import config
from .serializers import PasswordChangeSerializer, ProfileSerializer, ProfileUpdateSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        confirmation = request.data.get('confirm')
        if confirmation != 'yes':
            return Response({"error": "Please confirm account deletion by sending 'yes'."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        user_email = user.email

        send_mail(
            subject="Account Deletion Confirmation",
            message=f"Hello {user.username},\n\nYour account has been permanently deleted.\n\nIf this was not you, contact support immediately.",
            from_email=config('EMAIL_HOST_USER'),
            recipient_list=[user_email],
            fail_silently=False
        )

        user.delete()

        return Response({"message":"your account is deleted permanently"}, status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)

        if request.user != user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)