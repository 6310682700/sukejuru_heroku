from re import template
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


# Create your views here.

def index(request):
    about = loader.get_template('about.html')
    return HttpResponse(about.render())