from django.shortcuts import render
from django.http import HttpResponse
from html.parser import HTMLParser

def index(request):
    return HttpResponse("<a href='/rango/about/'>About</a>")
    
def about(request):
    return HttpResponse("<a href = '/rango/'>Index</a>")
