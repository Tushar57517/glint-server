from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"verification link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
    

class VerifyEmailView(APIView):
    def get(self, request):
        token = request.GET.get('token')

        try:
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])

            user.is_active = True
            user.save()

            return Response({"message":"email verified successfully"}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data

            refresh = RefreshToken.for_user(user)
            return Response({"refresh":str(refresh), "access":str(refresh.access_token)}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"message":"refresh token required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({"access":access_token}, status=status.HTTP_200_OK)
        
        except Exception:
            return Response({"error":"Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')

            if not refresh_token:
                return Response({"error":"refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message":"successfully logged out"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error":"invalid token"}, status=status.HTTP_400_BAD_REQUEST)