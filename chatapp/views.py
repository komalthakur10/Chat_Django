# views.py in django is used to process user request and to respond to it

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Msg
from . forms import UserSignupForm
from . forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages      
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    user_list = User.objects.all() 
    user_list = user_list.exclude(id = 1) # admin
    user_list = user_list.exclude(id = request.user.id) # logged in user
    prof_list = Profile.objects.all()
    context = {
        "user_list" : user_list,
        "prof_list": prof_list
            }
#    print(context)
    return render(request, "chatapp/Home.html", context)

def signup(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account created successfully")
            return redirect("Login")
    else:
        form = UserSignupForm()
    return render(request, "chatapp/Signup.html", {"form":form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Account has been updated!")
            return redirect("Profile")
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,"chatapp/Profile.html", context)