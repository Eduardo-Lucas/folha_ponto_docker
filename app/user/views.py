import json

from apontamento.models import Ponto, TipoReceita
from apontamento.views import fecha_tarefa
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy  # type: ignore
from django.views.generic.edit import UpdateView
from user.forms import LoginForm, UserProfileform

from .models import UserProfile


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
                # get name from UserProfile
                try:
                    user_profile = UserProfile.objects.get(user=user)
                except ObjectDoesNotExist:
                    user_profile = UserProfile(user=user)
                    user_profile.tipo_receita = TipoReceita.objects.get(id=1)
                    user_profile.save()

                if user.email is None or user.email == "":
                    messages.warning(request, "Por favor, atualize seu E-mail. Acesse 'Meu Perfil' no menu superior.")

                if user_profile.nome is None or user_profile.nome == "":
                    messages.warning(request, "Por favor, atualize seu perfil.")
                else:
                    messages.success(
                        request, f"Olá {user_profile.nome}, seja bem-vindo de volta!"
                    )
                return redirect("core:home")

        # form is not valid or user is not authenticated
        messages.error(request, "Invalid username or password")
        return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """View for logging out a user."""

    verificar_tarefas_abertas(request)

    logout(request)
    messages.success(request, "Você foi desconectado.")
    return redirect("user:login")


class PasswordsChangeView(PasswordChangeView):
    """View for changing a user's password."""

    form_class = PasswordChangeForm
    success_url = reverse_lazy("user:success_password")


def success_password(request):
    """View for successful password change."""
    return render(request, "registration/success_password.html")


@login_required
def verificar_tarefas_abertas(request):
    """View for checking open tasks."""
    open_tasks = Ponto.objects.get_open_pontos(user=request.user)

    if open_tasks:
        # close them
        for task in open_tasks:
            fecha_tarefa(request, task.id)
        return True
    return False


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """View for a user's profile."""

    template_name = "registration/profile.html"
    model = User
    form_class = UserProfileform
    success_url = reverse_lazy("user:profile")

    def get_object(self, queryset=None):
        """Get the user's profile."""
        return get_object_or_404(UserProfile, user=self.request.user)

    def form_valid(self, form):
        """Save the user's profile."""
        # check carga horaria between 1 and 8 hours
        carga_horaria = form.cleaned_data["cargahoraria"]
        if carga_horaria < 1 or carga_horaria > 8:
            messages.error(self.request, "Carga horária deve ser entre 1 e 8 horas.")
            return self.form_invalid(form)
        messages.success(self.request, "Seu perfil foi atualizado com sucesso.")
        form.instance.user = self.request.user
        return super().form_valid(form)


class AtualizaPerfil(LoginRequiredMixin, UpdateView):
    """View for a user's profile."""

    template_name = "registration/profile.html"
    model = User
    form_class = UserProfileform
    success_url = reverse_lazy("core:home")

    def get_object(self, queryset=None):
        """Get the user's profile."""
        # get the user id from url
        user_id = self.kwargs.get("pk")
        return get_object_or_404(UserProfile, user=user_id)

    def form_valid(self, form):
        carga_horaria = form.cleaned_data["cargahoraria"]
        if carga_horaria < 1 or carga_horaria > 8:
            messages.error(self.request, "Carga horária deve ser entre 1 e 8 horas.")
            return self.form_invalid(form)
        messages.success(self.request, "Seu perfil foi atualizado com sucesso.")

        return super().form_valid(form)


def usuario_autocomplete(request):
    """Autocomplete for Usuario"""
    data = None
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        query = request.GET.get("term", "")

        usuarios = User.objects.filter(username__icontains=query, is_active=True)

        results = []
        for usuario in usuarios:
            place_json = usuario.username

            results.append(place_json)

        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
