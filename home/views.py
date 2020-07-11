from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check for error
        myuser = User.objects.create_user(username,email,password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()
        messages.success(request, 'you have been successfully signed up!')
        return redirect('/')

    else:
        return HttpResponse('404 - Not Found')

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is None :
            messages.error(request, "invalid parameters")
            return redirect('/') 
        else:
            login(request, user)
            messages.success(request, "You have been successfully logged in!")
            return redirect('/')
    else:
        return HttpResponse('404 - Not Allowed')

    

def handleLogout(request):
    logout(request)
    messages.success(request, "You have been successfully Logout!")
    return redirect('index')