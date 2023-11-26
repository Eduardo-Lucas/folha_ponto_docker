from django.urls import path
from .views import *

app_name = "user"

urlpatterns = [
    path("login/", sign_in, name="login"),
    path("logout/", logout_view, name="logout"),
    path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),name='password_reset_complete'),

]
