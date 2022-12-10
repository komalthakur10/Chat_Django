from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # for login,logout,signup default view

urlpatterns = [

    path('', views.home, name='Home'),
    path('login/', auth_views.LoginView.as_view(template_name='chatapp/Login.html'), name='Login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='chatapp/Logout.html'), name='Logout'),
    path('signup/', views.signup, name='Signup'),
    path('profile/', views.profile, name='Profile')

]