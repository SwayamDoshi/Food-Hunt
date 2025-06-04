from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def add_user(request):
    return render(request, "users/signup.html")