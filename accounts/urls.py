from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from .views import register

from accounts.views import ProfileView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    path('register/', register, name='register'),
    # path('', include('django.contrib.auth.urls')),
]