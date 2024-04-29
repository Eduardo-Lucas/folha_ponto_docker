"""
Views para o app refeicao
"""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from refeicao.forms import RefeicaoForm

from .models import Refeicao


class RefeicaoListView(LoginRequiredMixin, ListView):
    """ "Lista de refeições"""

    model = Refeicao
    template_name = "refeicao_list.html"
    context_object_name = "refeicoes"
    paginate_by = 10

    def get_queryset(self):
        return Refeicao.objects.all().order_by("-data_refeicao")


class RefeicaoCreateView(LoginRequiredMixin, CreateView):
    """View para criar refeição"""

    model = Refeicao
    template_name = "refeicao_form.html"
    form_class = RefeicaoForm
    success_url = reverse_lazy("refeicao:refeicao_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user

        query = Refeicao.objects.get_queryset_usuario_data(
            self.request.user, form.instance.data_refeicao
        )
        if query.count() > 0:
            messages.error(
                self.request,
                "Refeição já cadastrada para esta data!",
            )
            return super().form_invalid(form)
        return super().form_valid(form)


class RefeicaoUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualizar refeição"""

    model = Refeicao
    template_name = "refeicao_form.html"
    form_class = RefeicaoForm
    success_url = reverse_lazy("refeicao:refeicao_list")


class RefeicaoDeleteView(LoginRequiredMixin, DeleteView):
    """View para deletar refeição"""

    model = Refeicao
    template_name = "refeicao_confirm_delete.html"
    success_url = reverse_lazy("refeicao:refeicao_list")


class RefeicaoDetailView(LoginRequiredMixin, DetailView):
    """View para detalhes de refeição"""

    model = Refeicao
    template_name = "refeicao_detail.html"
    context_object_name = "refeicao"


class SearchRefeicaoResultsView(ListView):
    """View para listar as férias filtradas."""

    paginate_by = 10
    model = Refeicao
    template_name = "refeicao_list.html"
    context_object_name = "refeicoes"

    def get_queryset(self):  # new
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            refeicoes = Refeicao.objects.filter(Q(usuario__username__icontains=query))
        else:  # pragma: no cover
            refeicoes = Refeicao.objects.all()

        return refeicoes
