"""
 Cadastro pare registro de Férias
"""

from datetime import timedelta

import numpy as np
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from ferias.forms import FeriasForm
from ferias.models import Ferias
from folha_ponto.settings import FERIAS_BUSINESS_DAYS


class FeriasListView(LoginRequiredMixin, ListView):
    """View para listar as férias."""

    model = Ferias
    template_name = "ferias/ferias_list.html"
    context_object_name = "ferias"
    paginate_by = 10

    def get_queryset(self):
        """Retorna o queryset de férias do usuário logado."""
        # if superuser, return all vacations
        if self.request.user.is_superuser:
            return Ferias.objects.all()
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

        # check if the year between data_inicial and data_final is the same
        if form.instance.data_inicial.year != form.instance.data_final.year:
            form.add_error(
                "data_inicial",
                "O período de férias deve ser no mesmo ano.",
            )
            return self.form_invalid(form)

        # 0. check if the period is equal or greater then the current year
        if form.instance.data_inicial.year < form.instance.periodo:
            form.add_error(
                "data_inicial",
                "O período de férias não pode ser menor que o ano atual.",
            )
            return self.form_invalid(form)

        # 1. check if data_inicial is greater than data_final
        if form.instance.data_inicial > form.instance.data_final:
            form.add_error(
                "data_inicial",
                "A data inicial não pode ser maior que a data final.",
            )
            return self.form_invalid(form)

        # 2. check if there is any other vacation in the same period
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

        # 3. check if the vacation period is greater than 20 days
        dias_uteis = np.busday_count(
            form.instance.data_inicial, form.instance.data_final + timedelta(days=1)
        )
        dias_uteis = int(dias_uteis)
        saldo_anterior = Ferias.objects.get_ferias_anteriores(
            data_inicial=form.instance.data_inicial,
            data_final=form.instance.data_final,
            user=self.request.user
        )
        if (timedelta(days=dias_uteis) + timedelta(days=int(saldo_anterior))) > timedelta(
            days=FERIAS_BUSINESS_DAYS
        ):
            # ferias can not be more than 20 days
            form.add_error(
                "data_final",
                f"O período de férias não pode ser maior que {FERIAS_BUSINESS_DAYS} dias úteis.",
            )
            return self.form_invalid(form)

        # 4. check if there is a previous vacation and there is still days to take
        ferias_anteriores = Ferias.objects.filter(
            user=self.request.user,
            data_final__lt=form.instance.data_inicial,
        )
        if ferias_anteriores.exists():

            if saldo_anterior + dias_uteis > FERIAS_BUSINESS_DAYS:
                form.add_error(
                    "data_inicial",
                    f"O período de férias não pode ser maior que {FERIAS_BUSINESS_DAYS} dias úteis.",
                )
                return self.form_invalid(form)

        form.instance.user = self.request.user
        form.instance.dias_uteis = dias_uteis

        return super().form_valid(form)

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")


class FeriasUpdateView(LoginRequiredMixin, UpdateView):
    """View para atualização de férias."""

    model = Ferias
    form_class = FeriasForm
    template_name = "ferias/ferias_form.html"

    def get_form_kwargs(self):
        kwargs = super(FeriasUpdateView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")

    def form_valid(self, form):
        """Se o formulário for válido, salva o objeto e redireciona para a URL de sucesso."""
        if form.instance.data_inicial > form.instance.data_final:
            form.add_error(
                "data_inicial",
                "A data inicial não pode ser maior que a data final.",
            )
            return self.form_invalid(form)

        # check if the year between data_inicial and data_final is the same
        if form.instance.data_inicial.year != form.instance.data_final.year:
            form.add_error(
                "data_inicial",
                "O período de férias deve ser no mesmo ano.",
            )
            return self.form_invalid(form)

        # 0. check if the period is equal or greater then the current year
        if form.instance.data_inicial.year < form.instance.periodo:
            form.add_error(
                "data_inicial",
                "O período de férias não pode ser menor que o ano atual.",
            )
            return self.form_invalid(form)

        dias_uteis = np.busday_count(
            form.instance.data_inicial, form.instance.data_final + timedelta(days=1)
        )
        dias_uteis = int(dias_uteis)
        saldo_anterior = Ferias.objects.get_ferias_anteriores(
            data_inicial=form.instance.data_inicial,
            data_final=form.instance.data_final,
            user=self.request.user
        )

        if (timedelta(days=dias_uteis) + timedelta(days=saldo_anterior)) > timedelta(
            days=FERIAS_BUSINESS_DAYS
        ):
            # ferias can not be more than 20 days
            form.add_error(
                "data_final",
                f"O período de férias não pode ser maior que {FERIAS_BUSINESS_DAYS} dias úteis.",
            )
            return self.form_invalid(form)

        # check if there is any other vacation in the same period and sum up more than 20 days
        ferias_no_periodo = Ferias.objects.filter(
            user=self.request.user,
            data_inicial__lte=form.instance.data_final,
            data_final__gte=form.instance.data_inicial,
        )
        if ferias_no_periodo.exists():
            saldo_anterior = Ferias.objects.get_ferias_anteriores(
                data_inicial=form.instance.data_inicial,
                data_final=form.instance.data_final,
                user=self.request.user
            )
            if saldo_anterior + form.instance.dias_uteis > FERIAS_BUSINESS_DAYS:
                form.add_error(
                    "data_inicial",
                    f"O período de férias não pode ser maior que {FERIAS_BUSINESS_DAYS} dias.",
                )
                return self.form_invalid(form)

        # check if there is any other vacation in the same period
        if (
            Ferias.objects.filter(
                user=self.request.user,
                data_inicial__lte=form.instance.data_final,
                data_final__gte=form.instance.data_inicial,
            )
            .exclude(id=self.object.id)
            .exists()
        ):
            form.add_error(
                "data_inicial",
                "Já existe um registro de férias para este período.",
            )
            return self.form_invalid(form)

        # check  if there is still balance for that period
        if (
            form.instance.data_inicial.year != form.instance.periodo
            or form.instance.data_final.year != form.instance.periodo
        ):
            # check if the previous vacation has balance yet
            if dias_uteis + saldo_anterior > FERIAS_BUSINESS_DAYS:
                form.add_error(
                    "data_inicial",
                    f"O período de {form.instance.periodo} não possui mais saldo!",
                )
                return self.form_invalid(form)

        form.instance.periodo = form.instance.data_inicial.year

        form.instance.dias_uteis = dias_uteis

        return super().form_valid(form)


class FeriasDeleteView(LoginRequiredMixin, DeleteView):
    """View para exclusão de férias."""

    model = Ferias
    template_name = "ferias/ferias_confirm_delete.html"

    def get_success_url(self):
        """Retorna a URL de sucesso."""
        return reverse("ferias:ferias_list")


class SearchFeriasResultsView(ListView):
    """View para listar as férias filtradas."""

    paginate_by = 11
    model = Ferias
    template_name = "ferias/search_ferias_results.html"
    context_object_name = "search_ferias"

    def get_queryset(self):  # new
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get("q")
            search_ferias = Ferias.objects.filter(Q(user__username__icontains=query))
        else:  # pragma: no cover
            search_ferias = Ferias.objects.all()

        return search_ferias
