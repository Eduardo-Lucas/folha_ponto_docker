import json

from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Cliente, ClienteTipoSenha
from .forms import ClienteForm, ClienteTipoSenhaForm


def cliente_autocomplete(request):
    """Autocomplete for cliente"""
    data = None
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        query = request.GET.get("term", "")

        if query.isdigit():
            clientes = Cliente.objects.filter(
                codigosistema__exact=int(query), situacaoentidade=1
            )
        else:
            clientes = Cliente.objects.filter(
                nomerazao__icontains=query, situacaoentidade=1
            )

        results = []
        for cliente in clientes:
            if cliente.codigosistema:
                place_json = f"{cliente.codigosistema.zfill(4)}|{cliente.nomerazao}"
            else:
                place_json = cliente.nomerazao

            results.append(place_json)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/cliente_form.html"
    success_url = reverse_lazy("cliente:cliente_list")

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.instance.id = Cliente.objects.last().id + 1
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo Cliente"
        return context

class ClienteListView(LoginRequiredMixin, ListView):
    """ Lista de Cliente Ativo"""

    model = Cliente
    template_name = "cliente/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        object_list = Cliente.objects.cliente_ativo().order_by("nomerazao", )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        return context



class ClienteInativoListView(LoginRequiredMixin, ListView):
    """ Lista de Cliente Inativo"""

    model = Cliente
    template_name = "cliente/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        object_list = Cliente.objects.cliente_inativo().order_by("nomerazao", )
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/cliente_form.html"
    success_url = reverse_lazy("cliente:cliente_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Cliente"
        return context


# Item de Segurança
class ClienteTipoSenhaListView(LoginRequiredMixin, ListView):
    model = ClienteTipoSenha
    template_name = "cliente/clientetiposenha_list.html"
    context_object_name = "clientetiposenhas"
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = ClienteTipoSenha.objects.filter(
                Q(cliente__nomerazao__icontains=query)
            ).order_by("cliente__nomerazao")
        else:
            object_list = ClienteTipoSenha.objects.all().order_by("cliente__nomerazao")
        return object_list

class ClienteTipoSenhaCreateView(LoginRequiredMixin, CreateView):
    model = ClienteTipoSenha
    form_class = ClienteTipoSenhaForm
    template_name = "cliente/clientetiposenha_form.html"
    success_url = reverse_lazy("cliente:cliente_tipo_senha_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Novo Item de Segurança"
        return context

class ClienteTipoSenhaUpdateView(LoginRequiredMixin, UpdateView):
    model = ClienteTipoSenha
    form_class = ClienteTipoSenhaForm
    template_name = "cliente/clientetiposenha_form.html"
    success_url = reverse_lazy("cliente:cliente_tipo_senha_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Item de Segurança"
        return context

class ClienteTipoSenhaDeleteView(LoginRequiredMixin, DeleteView):
    model = ClienteTipoSenha
    template_name = "cliente/clientetiposenha_confirm_delete.html"
    success_url = reverse_lazy("cliente:cliente_tipo_senha_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Excluir Item de Segurança"
        return context
