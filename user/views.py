from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Profile
from .forms import *


# LOGIN user to application
def loginUser(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        
        try:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            message.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect')
    
    return render(request, 'user/login_register.html')

def logoutUser(request):
    logout(request) #delete session
    messages.success(request, 'Logout success')
    return redirect('home')

# Register user to application
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occurred during registration")

    context = {
        'page': page,
        'form': form,
    }
    return render(request, 'user/login_register.html', context)

def home(request):
    return render(request, 'index.html',)

@login_required(login_url="login")
def account(request):
    profile = request.user.profile
    name = request.user.first_name
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Update Profile Success")
            return redirect('account')

    context = {
        'name': name,
        'form': form,
    }
    return render(request, 'user/account.html', context)


