from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import Group

# Register your models here.

admin.site.unregister(Group)

admin.site.register(Profile)

