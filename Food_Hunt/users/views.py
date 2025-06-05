from django.shortcuts import render
from django.http import HttpResponse
from .models import Users

# Create your views here.
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
                context["msg"] = "Password and confirm Password must be same"
                return render(request, "users/signup.html", context)
            
            if password != cpassword : 
                context["msg"] = "Password and confirm Password must be same"
                return render(request, "users/signup.html", context)
            
            user = Users(user_name = user_name,user_type = user_type, email_ID = email_ID)
            user.set_password(password)
            user.save()

            context["msg"] = "Inserted Successfully"
            context["user_name"] = ""
            context["user_type"] = ""
            context["email_ID"] = ""

            return render(request, "users/signup.html",context)
        
        except Exception as e:
            context["msg"] = str(e)
            return render(request, "users/signup.html", context)
    return render(request, "users/signup.html")




def home(request):
    return render(request, "home.html")