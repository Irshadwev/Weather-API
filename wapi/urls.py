from django.urls import path
from . import views

urlpatterns = [
    # Frontend weather application
    path("weather-app/", views.weather_page, name="weather-page"),

    # Weather API
    path("weather/", views.weather, name="weather-api"),
]