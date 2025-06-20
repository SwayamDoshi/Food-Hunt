from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Restaurant
from users.models import Users
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from .models import Menu
from .models import Thali
from .models import ThaliItem


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


def home(request):
    return render(request, "home.html")

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/users/login')

    current_user = Users.objects.get(user_id=request.session['user_id'])
    
    if current_user.user_type == 'user':
        return HttpResponse("You're not authorize to access this page")
    menus = Menu.objects.filter(restaurant=current_user, created_at=date.today())
    return render(request, "restaurant/dashboard.html", {"menus": menus})


def res_landing_page(request):
    if 'user_id' not in request.session:
        return redirect('/users/login')

    restaurant = Users.objects.get(user_id=request.session['restaurant_id'])
    thalis = Thali.objects.filter(restaurant=restaurant, created_at=date.today())

    return render(request, "restaurant/dashboard.html", {
        "restaurant": restaurant,
        "thalis": thalis
    })


# def res_landing_page(request):
#     if 'restaurant_id' not in request.session:
#         return redirect('restaurant_login')

#     restaurant = Users.objects.get(user_id=request.session['restaurant_id'])

#     today = date.today()
#     menus = Menu.objects.filter(restaurant=restaurant, created_at=today)

#     return render(request, "restaurant/dashboard.html", {
#         "restaurant": restaurant,
#         "menus": menus
#     })

# def res_landing_page(request):
#     if 'restaurant_id' not in request.session:
#         return redirect('restaurant_login')

#     restaurant = Users.objects.get(id=request.session['restaurant_id'])
#     menus = Menu.objects.filter(restaurant=restaurant, created_at=date.today())

#     return render(request, "restaurant/dashboard.html", {"menus": menus})

# def add_thali(request):
#     if request.method == "POST":
#         thali_name = request.POST.get("thali_name")
#         price = request.POST.get("price")
#         items = request.POST.getlist("items")  # Multiple items

#         restaurant = Users.objects.get(user_id=request.session['restaurant_id'])
#         thali = Thali.objects.create(restaurant=restaurant, thali_name=thali_name, price=price)

#         for item in items:
#             ThaliItem.objects.create(thali=thali, item_name=item)

#         return redirect("res_landing_page")
#     return render(request, "restaurant/add_thali.html")



def add_menu_item(request):
    if request.method == "POST":
        item_name = request.POST.get("item_name")
        price = request.POST.get("price")
        description = request.POST.get("description")

        restaurant = Users.objects.get(user_id = request.session['user_id'])

        Menu.objects.create(
            restaurant = restaurant,
            item_name = item_name,
            price = price,
            description = description
        )
        return redirect("res_landing_page/")
    return redirect("res_landing_page/")


def delete_menu_item(request,id):
    Menu.objects.filter(user_id=id).delete()
    return redirect("res_landing_page")


def logout_view(request):
    request.session.flush()
    return redirect('/users/login')