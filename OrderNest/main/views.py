from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse


# Create your views here.

def home_view(request:HttpRequest):

    return render(request, "home.html")

def about_view(request):
    return render(request, "about.html")