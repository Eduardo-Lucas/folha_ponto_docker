"""
 Cadastro pare registro de Férias
"""
from datetime import timedelta
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

    def get_form_kwargs(self):
        kwargs = super(FeriasCreateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


    def form_valid(self, form):
        """Se o formulário for válido, salva o objeto e redireciona para a URL de sucesso."""
        form.instance.user = self.request.user
        if form.instance.data_inicial > form.instance.data_final:
            form.add_error(
                "data_inicial",
                "A data inicial não pode ser maior que a data final.",
            )
            return self.form_invalid(form)

        if (form.instance.data_final - form.instance.data_inicial) + timedelta(days=1) > timedelta(days=20):
            # ferias can not be more than 20 days
            form.add_error(
                "data_final",
                "O período de férias não pode ser maior que 20 dias.",
            )
            return self.form_invalid(form)

        # check if there is any other vacation in the same period
        if Ferias.objects.filter(
            user=self.request.user,
            data_inicial__lte=form.instance.data_final,
            data_final__gte=form.instance.data_inicial,
        ).exists():
            form.add_error(
                "data_inicial",
                "Já existe um registro de férias para este período.",
            )
            return self.form_invalid(form)

        form.instance.user = self.request.user
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
