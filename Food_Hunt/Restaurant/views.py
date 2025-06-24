from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Menu, Item, Restaurant
from users.models import Users
from django.contrib.auth.hashers import make_password, check_password
from datetime import timedelta
from django.contrib import messages
# from .models import Menu

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

            return redirect("/users/login")

        except Exception as e:
            context["msg"] = f"An error occurred: {str(e)}"
            return render(request, "restaurant/signup.html", context)

    return render(request, "restaurant/signup.html")

def home(request):
    return render(request, "home.html")

def logout_view(request):
    request.session.flush()
    return redirect("restaurant_login")


from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Menu, Item, Restaurant

def add_menu(request):
    if request.method == 'POST':
        dishName = request.POST.get('dishName')
        meal_type = request.POST.get('meal_type')
        price = request.POST.get('price')
        time_limit = request.POST.get('time_limit')
        description = request.POST.get('description')
        picture = request.FILES.get('picture')

        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "User not found in session.")
            return redirect('/restaurant/add_menu')

        try:
            restaurant = Restaurant.objects.get(user_id=user_id)
        except Restaurant.DoesNotExist:
            messages.error(request, "Restaurant not found for this user.")
            return redirect('/restaurant/add_menu')

        try:
            hours, minutes, seconds = map(int, time_limit.split(":"))
            time_limit = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            messages.error(request, "Invalid time format.")
            return redirect('/restaurant/add_menu')

        menu = Menu.objects.create(
            restaurant = restaurant,
            dishName = dishName,
            meal_type = meal_type,
            price = price,
            time_limit = time_limit,
            description = description,
            picture = picture
        )

        for key in request.POST:
            if key.startswith("item_name_"):
                item_name = request.POST.get(key)
                if item_name:
                    Item.objects.create(menu=menu, item_name=item_name)

        messages.success(request, "Menu and items added successfully!")
        return redirect('/restaurant/add_menu')

    return render(request, 'restaurant/add_menu.html')


    
def view_menu(request):
    return render(request, "restaurant/view_menu.html")