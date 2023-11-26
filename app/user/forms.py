from django import forms


class LoginForm(forms.Form):
    """Login Form"""
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
