from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def add_restaurant(request):
    return render(request, "restaurant/signup.html")