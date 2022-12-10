"""Web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.conf.urls.static import static                         # for image field
from django.conf import settings                                   

from django.contrib.staticfiles.storage import staticfiles_storage # for favicon
from django.views.generic.base import RedirectView        

from rest_framework.routers import DefaultRouter                   # for viewset 
from chatapp.api import MsgViewSet
from django.views.generic import TemplateView
router = DefaultRouter() 
router.register(r'msg', MsgViewSet, basename='msg-api')                                     

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatapp.urls')),
    path(r'api/v1/', include(router.urls)),                        # for viewset
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('chatapp/logo.png'))) #   site logo
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)