from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy  # type: ignore
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView


def sign_in(request):
    """View for signing in a user."""
    if request.method == "GET":
        form = LoginForm()
        return render(request, "registration/login.html", {"form": form})
    elif request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Hi {username.title()}, welcome back!")
                return redirect("core:home")

        # form is not valid or user is not authenticated
        messages.error(request, "Invalid username or password")
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """View for logging out a user."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("user:login")


class PasswordsChangeView(PasswordChangeView):
    """View for changing a user's password."""

    form_class = PasswordChangeForm
    success_url = reverse_lazy("user:success_password")


def success_password(request):
    """View for successful password change."""
    return render(request, "registration/success_password.html")
