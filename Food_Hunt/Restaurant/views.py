from django.shortcuts import redirect
from django.shortcuts import render
from .models import Restaurant
from users.models import Users
from django.http import HttpResponse
from django.contrib import messages
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


def add_restaurant(request):
    return render(request, "restaurant/signup.html")


def restaurant_signup_view(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            usertype = request.POST.get('usertype')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            res_name = request.POST.get('res_name')
            res_number = request.POST.get('res_number')
            res_address = request.POST.get('res_address')
            fssai_no = request.POST.get('fssai_no')
            res_cat = request.POST.get('res_cat')
            res_picture = request.FILES.get('res_picture')

            if password != confirm_password:
                return HttpResponse("Error: Passwords do not match")

            # if Users.objects.filter(user_name=username).exists():
            #     return render(request, "restaurant/signup.html", {"msg": "Username already exists"})

            # if Users.objects.filter(email_ID=email).exists():
            #     return render(request, "restaurant/signup.html", {"msg": "Email already exists"})

            user = Users.objects.create(
                user_name=username,
                user_type=usertype,
                email_ID=email,
                password=make_password(password)
            )

            Restaurant.objects.create(
                user_id = user,
                res_number=res_number,
                res_name=res_name,
                res_address=res_address,
                fssai_no=fssai_no,
                res_picture=res_picture,
                res_cat=res_cat
            )

            return render(request, 'restaurant/restaurant_login.html')

        except Exception as e:
            return HttpResponse(f"Error occurred: {str(e)}")

    return render(request, 'restaurant/restaurant_login.html')

def restaurant_login_view(request):
    msg="to login page"
    return HttpResponse(msg)