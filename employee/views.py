from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db import connection
from .models import employee, city, state, country
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'login.html')
# Create your views here.
def listing(request):
    return render(request,'employee-record.html')	
