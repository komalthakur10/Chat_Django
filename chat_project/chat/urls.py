from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage, name='Chat-homepage'),
    path('login/', views.Login, name='Chat-login'),
    path('registration/', views.Registration, name='Chat-registration'),
    path('home/', views.Home, name='Chat-home'),
    path('about/', views.About, name='Chat-about'),
]