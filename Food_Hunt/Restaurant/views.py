from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant
from users.models import Users
from django.contrib.auth.hashers import make_password, check_password

def restaurant_signup_view(request):
    if request.method == 'POST':
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

        context = {
            "username": username,
            "usertype": usertype,
            "email": email,
            "res_name": res_name,
            "res_number": res_number,
            "res_address": res_address,
            "fssai_no": fssai_no,
            "res_cat": res_cat,
        }

        try:
            if not all([username, usertype, email, password, confirm_password, res_name, res_number, res_address, fssai_no, res_cat]):
                context["msg"] = "Please fill all the details"
                return render(request, "restaurant/signup.html", context)

            if password != confirm_password:
                context["msg"] = "Password and confirm password must be same"
                return render(request, "restaurant/signup.html", context)

            if Users.objects.filter(email_ID=email).exists():
                context["msg"] = "Email already registered"
                return render(request, "restaurant/signup.html", context)

            user = Users.objects.create(
                user_name=username,
                user_type=usertype,
                email_ID=email,
                password=make_password(password)
            )

            Restaurant.objects.create(
                user_id=user,
                res_name=res_name,
                res_number=res_number,
                res_address=res_address,
                fssai_no=fssai_no,
                res_cat=res_cat,
                res_picture=res_picture
            )

            return redirect("/restaurant/login")

        except Exception as e:
            context["msg"] = f"An error occurred: {str(e)}"
            return render(request, "restaurant/signup.html", context)

    return render(request, "restaurant/signup.html")



def login(request):
    if request.method == "POST":
        email_ID = request.POST.get('email_ID')
        password = request.POST.get('password')

        context = {
            "email_ID": email_ID,
        }

        try:
            if email_ID == "" or password == "":
                context["msg"] = "Email and password required"
                return render(request, "restaurant/login.html", context)

            user = Users.objects.get(email_ID=email_ID, user_type="restaurant")

            if check_password(password, user.password):
                # return redirect("/landing_page")
                return redirect("/restaurant/landing_page")
            else:
                context["msg"] = "Invalid credentials"
                return render(request, "restaurant/login.html", context)

        except Users.DoesNotExist:
            context["msg"] = "Restaurant user does not exist"
            return render(request, "restaurant/login.html", context)

    return render(request, "restaurant/login.html")

def home(request):
    return render(request, "home.html")

def res_landing_page(request):
    return HttpResponse("<h1>this is the restaurant dashbord</h1>")
