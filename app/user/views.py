from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy # type: ignore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import SetPasswordForm
from .forms import LoginForm


def sign_in(request):
    """View for signing in a user."""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "registration/login.html", {'form': form})
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
        return render(request,'registration/login.html',{'form': form})


def logout_view(request):
    """View for logging out a user."""
    logout(request)
    messages.success(request,'You have been logged out.')
    return redirect("user:login")




@login_required
def change_password(request):
    """View for changing a user's password."""
    # Check if the user needs to change the password
    if request.user.has_usable_password():
        # If the user already has a usable password, redirect them to a different page
        messages.info(request,'You already have a password set.')
        return redirect('core:home')  # Replace 'some_other_view' with the desired view name or URL

    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:home')  # Redirect to a success page or another view after changing the password
    else:
        form = SetPasswordForm(request.user)

    return render(request, 'registration/change_password.html', {'form': form})
