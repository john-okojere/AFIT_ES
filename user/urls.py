from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from user import views

urlpatterns = [
   path('profile/', views.user_profile, name='user_profile'),
]
