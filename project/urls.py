"""
# URL configuration for project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from random import random
from django.http import HttpResponse
from app_datatime.views import datetime_view
from app_weather.views import weather_view
from store.views import products_view, shop_view


def random_view(request):
    if request.method == 'GET':
        data = random()
        return HttpResponse(data)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('random/', random_view),
    path('datetime/', datetime_view),
    path('weather/', weather_view),
    path('product/', products_view),
    path('', shop_view),
    path('', include('store.urls')),
    path('', include('app_weather.urls')),
    path('login/', include('app_login.urls')),  # маршруты приложений с помощью unclude
]
