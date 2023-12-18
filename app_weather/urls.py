from django.urls import path  # импорт. патч из корневой папки
from .views import weather_view  # импортируем из файла view def my_view


urlpatterns = [
    path('weather/', weather_view),
]