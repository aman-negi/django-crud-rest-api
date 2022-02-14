from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
# import requests

# Create your views here.

def Register(request):
    return render(request,'frontend/register.html')

def Login(request):
    return render(request,'frontend/login.html')

def Profile(request):
    return render(request,'frontend/profile.html')

def logout(request):
    return render(request,'frontend/loginhtml')
