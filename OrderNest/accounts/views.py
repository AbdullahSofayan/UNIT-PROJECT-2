from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse

# Create your views here.

def login_view(request:HttpRequest):

    return render(request, "login.html")