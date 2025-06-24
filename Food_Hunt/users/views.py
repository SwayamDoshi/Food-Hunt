from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Users

def add_user(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        user_type = request.POST.get('user_type')
        email_ID = request.POST.get('email_ID')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        context = {
            "user_name": user_name,
            "user_type": user_type,
            "email_ID": email_ID,
        }

        try:
            if user_name == "" or user_type == "" or email_ID == "" or password == "" or cpassword == "" : 
                context["msg"] = "Please fill all the details"
                return render(request, "users/signup.html", context)
            
            if password != cpassword : 
                context["msg"] = "Password and confirm Password must be same"
                return render(request, "users/signup.html", context)
            
            if Users.objects.filter(email_ID=email_ID).exists():
                context["msg"] = "Email already registered"
                return render(request, "users/signup.html", context)

            user = Users(user_name = user_name,user_type = user_type, email_ID = email_ID)
            user.set_password(password)
            user.save()

            context["msg"] = "Inserted Successfully"
            context["user_name"] = ""
            context["user_type"] = ""
            context["email_ID"] = ""

            return redirect("/users/login")
        
        except Exception as e:
            context["msg"] = str(e)
            return render(request, "users/signup.html", context)
    return render(request, "users/signup.html")

def login(request):
    if request.method == "POST":
        email_ID = request.POST.get('email_ID')
        password = request.POST.get('password')

        context = {
            "email_ID": email_ID,
            "password": password,
        }

        try:
            if email_ID == "" or password == "": 
                context["msg"] = "Email and password required"

            userExist = Users.objects.get(email_ID = email_ID)
            print("--------------------hello-------------------")
            print(userExist)
            if userExist.check_password(password):
                request.session['user_id'] = userExist.user_id
                request.session['user_email'] = userExist.email_ID
                request.session['user_type'] = userExist.user_type
                if userExist.user_type == 'restaurant':
                    return redirect('/restaurant/dashboard')
                return redirect('/')
            else:
                context["msg"] = "Invalid Credentials"
            return render(request, "users/login.html", context)
        
        except Users.DoesNotExist:
            context["msg"] = "User does not exist"
            return render(request, "users/login.html", context)

    return render(request, "users/login.html")

def dashboard(request):
    if request.session.get('user_type') == 'restaurant':
        return render(request, "restaurant/dashboard.html")
    else: 
        return HttpResponse("shu che bhai bohot shana ban raha hai !!")

def home(request):
    return render(request, "home.html")