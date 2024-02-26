"""
 Cadastro pare registro de Férias
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from ferias.forms import FeriasForm
from ferias.models import Ferias


class FeriasListView(LoginRequiredMixin, ListView):
    """View para listar as férias."""

    model = Ferias
    template_name = "ferias/ferias_list.html"
    context_object_name = "ferias"

    def get_queryset(self):
        """Retorna o queryset de férias do usuário logado."""
        return Ferias.objects.filter(user=self.request.user)


class FeriasCreateView(LoginRequiredMixin, CreateView):
    """View para cadastro de férias."""

    model = Ferias
    form_class = FeriasForm
    template_name = "ferias/ferias_form.html"

    def form_valid(self, form):
        """Se o formulário for válido, salva o objeto e redireciona para a URL de sucesso."""
        form.instance.user = self.request.user
        if form.instance.data_inicial > form.instance.data_final:
            form.add_error(
                "data_inicial",
                "A data inicial não pode ser maior que a data final.",
            )
            return self.form_invalid(form)

        if form.instance.user is None:
            form.add_error(
                None,
                "Usuário não informado.",
            )
            return self.form_invalid(form)

        return super().form_valid(form)

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")


class FeriasUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualização de férias."""

    model = Ferias
    form_class = FeriasForm
    template_name = "ferias/ferias_form.html"

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")


class FeriasDeleteView(LoginRequiredMixin, DeleteView):
    """View para exclusão de férias."""

    model = Ferias
    template_name = "ferias/ferias_confirm_delete.html"

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")
