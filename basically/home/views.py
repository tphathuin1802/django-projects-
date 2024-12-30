# home/views.py
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def room(request):
    return HttpResponse("Room")
