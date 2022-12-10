from django.shortcuts import render

# Create your views here.

def Homepage(request):
    return render(request,'chat/Homepage.html', {'title':'Homepage'})

def Login(request):
    return render(request,'chat/Login.html', {'title':'Login'})

def Registration(request):
    return render(request,'chat/Registration.html', {'title':'Registration'})

def Home(request):
    return render(request,'chat/Home.html', {'title':'Home'})

def About(request):
    return render(request,'chat/About.html', {'title':'About'})