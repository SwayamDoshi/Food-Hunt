"""
URL configuration for Food_Hunt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from users import views as user_views
from Restaurant import views as restaurant_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/add-user', user_views.add_user),
    path('restaurant/add-restaurant', restaurant_views.restaurant_signup_view),
    path('restaurant/login',user_views.login),
    path('users/login', user_views.login),
    path('', user_views.home),
    path('',restaurant_views.home),
    path('logout/',restaurant_views.logout_view,name="logout_view"),
]