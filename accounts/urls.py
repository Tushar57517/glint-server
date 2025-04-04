from django.urls import path
from .views import RegisterView, VerifyEmailView, LoginView, RefreshTokenView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]