from django.contrib import admin
from django.urls import path
from .views import CreateFlight
urlpatterns = [
    path("flight/create", CreateFlight.as_view())
]