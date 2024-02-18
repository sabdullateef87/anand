from django.contrib import admin
from django.urls import path
from .views import UserCreateView, VerifyEmail, Login, DummyAuthView, LogoutView, GetUserDetails
urlpatterns = [
    path('user/register', UserCreateView.as_view()),
    path('user/verify_email', VerifyEmail.as_view()),
    path('user/login', Login.as_view()),
    path('user/dummy', DummyAuthView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user/details/<', GetUserDetails.as_view())
]