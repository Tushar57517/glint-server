from django.urls import path
from .views import DeleteAccountView, ChangePasswordView, ProfileView, ProfileUpdateView

urlpatterns = [
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('<str:username>/', ProfileView.as_view(), name='user-profile'),
    path('<str:username>/update/', ProfileUpdateView.as_view(), name='user-profile-update'),
]
