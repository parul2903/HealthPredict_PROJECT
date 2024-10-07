from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


class UserLoginView(auth_views.LoginView):
    template_name = 'login.html'

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

def about(request):
    return render(request, 'about.html', {})

def doctors(request):
    return render(request, 'doctor.html',{})

def contact(request):
    return render(request, 'contact.html',{})

def register(request):
    if request.method == 'POST':
       username = request.POST['username'] 
       email = request.POST['email'] 
       password = request.POST['password'] 
       user = User.objects.create(username=username,email=email,password=make_password(password))
       user.save()
       return redirect('login')
    else:
        return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password'] 
        user = authenticate(username=username,password=password)
        # print(user)
        if user is not None:
            login(request,user)
            return redirect('profile')
        else:
            return redirect('login')
    else:
        return render(request,'login.html')


def profile(request):
    return render(request, 'profile.html')


