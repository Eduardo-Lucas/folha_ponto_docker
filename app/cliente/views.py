import json

from django.db.models import Q
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from .models import Cliente, ClienteTipoSenha, TipoSenha
from .forms import ClienteFilterForm, ClienteForm, ClienteTipoSenhaForm
from .filters import ClienteFilter
from django.db.models import Max
from django.db.models.functions import Length
from django.db.models.functions import Length


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

        # check if codigosistema already exists
        if form.instance.codigosistema:
            if Cliente.objects.filter(codigosistema=form.instance.codigosistema).exists():
                form.add_error("codigosistema", "Código já existe.")
                return self.form_invalid(form)

        # check if codigosistema has length 4 and the first character is a zero, cut it off
        if form.instance.codigosistema and form.instance.codigosistema[0] == "0":
            form.instance.codigosistema = form.instance.codigosistema[1:]

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
        self.filterset = ClienteFilter(self.request.GET, queryset=object_list)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        context["filter"] = self.filterset
        context['qtd_cpf'] = Cliente.objects.filter(situacaoentidade=1, tipodocumento=1).count()
        context['qtd_cnpj'] = Cliente.objects.filter(situacaoentidade=1, tipodocumento=2).count()
        return context



class ClienteInativoListView(LoginRequiredMixin, ListView):
    """ Lista de Cliente Inativo"""

    model = Cliente
    template_name = "cliente/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        object_list = Cliente.objects.cliente_inativo().order_by("nomerazao", )
        self.filterset = ClienteFilter(self.request.GET, queryset=object_list)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Clientes"
        context["filter"] = self.filterset
        context['qtd_cpf'] = Cliente.objects.filter(tipodocumento=1).exclude(situacaoentidade=1).count()
        context['qtd_cnpj'] = Cliente.objects.filter(tipodocumento=2).exclude(situacaoentidade=1).count()

        return context

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cliente/cliente_form.html"
    success_url = reverse_lazy("cliente:cliente_list")

    def form_valid(self, form):
        # check if codigosistema has length 4 and the first character is a zero, cut it off
        if form.instance.codigosistema and form.instance.codigosistema[0] == "0":
            form.instance.codigosistema = form.instance.codigosistema[1:]

        return super().form_valid(form)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Itens de Segurança"
        context["cliente_id"] = self.kwargs.get("cliente_id")
        try:
            context["nomerazao"] = Cliente.objects.get(id=self.kwargs.get("cliente_id"))
        except Cliente.DoesNotExist:
            context["nomerazao"] = None
        return context

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            object_list = ClienteTipoSenha.objects.filter(
                Q(cliente__nomerazao__icontains=query)
            ).order_by("cliente__nomerazao")
        else:
            # filter by cliente_id
            object_list = ClienteTipoSenha.objects.filter(cliente=self.kwargs.get("cliente_id")).order_by("cliente__nomerazao")

        return object_list

class ClienteTipoSenhaCreateView(LoginRequiredMixin, CreateView):
    model = ClienteTipoSenha
    form_class = ClienteTipoSenhaForm
    template_name = "cliente/clientetiposenha_form.html"
    context_object_name = "clientetiposenha"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs["cliente_id"] = self.kwargs.get("cliente_id")
        return kwargs

    def get_success_url(self):
        return reverse_lazy("cliente:cliente_tipo_senha_list", kwargs={"cliente_id": self.kwargs.get("cliente_id")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Cadastrar Senha"
        context["cliente_id"] = self.kwargs.get("cliente_id")
        context["nomerazao"] = Cliente.objects.get(id=self.kwargs.get("cliente_id"))
        return context

    def form_valid(self, form):
        try:
            form.cliente = Cliente.objects.get(id=self.kwargs.get("cliente_id"))
            form.tipo_senha = TipoSenha.objects.get(id=form.instance.tipo_senha.id)
            return super().form_valid(form)
        except Cliente.DoesNotExist:
            form.add_error(None, "Cliente não encontrado.")
            return self.form_invalid(form)



class ClienteTipoSenhaUpdateView(LoginRequiredMixin, UpdateView):
    model = ClienteTipoSenha
    form_class = ClienteTipoSenhaForm
    template_name = "cliente/clientetiposenha_form.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs()
        kwargs["cliente_id"] = self.kwargs.get("cliente_id")
        return kwargs

    def get_success_url(self):
        return reverse_lazy("cliente:cliente_tipo_senha_list", kwargs={"cliente_id": self.kwargs.get("cliente_id")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Editar Senha"
        context["cliente_id"] = self.kwargs.get("cliente_id")
        context["nomerazao"] = Cliente.objects.get(id=self.kwargs.get("cliente_id"))
        return context



class ClienteTipoSenhaDeleteView(LoginRequiredMixin, DeleteView):
    model = ClienteTipoSenha
    template_name = "cliente/clientetiposenha_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("cliente:cliente_tipo_senha_list", kwargs={"cliente_id": self.kwargs.get("cliente_id")})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Excluir Item de Segurança"
        context["cliente_id"] = self.kwargs.get("cliente_id")
        context["nomerazao"] = Cliente.objects.get(id=self.kwargs.get("cliente_id"))
        return context
