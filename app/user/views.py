from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib import messages

from .forms import LoginForm

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


def sign_in(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "user/login.html", {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('core:home')

        # form is not valid or user is not authenticated
        messages.error(request,'Invalid username or password')
        return render(request,'user/login.html',{'form': form})


def logout_view(request):
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect("user:login")
