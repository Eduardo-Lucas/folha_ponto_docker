from datetime import datetime, time, timedelta

from utils.last_day_of_month import get_last_day_of_month
from cliente.models import Cliente
from django.contrib.auth.models import User
from django.db.models import Count, Sum, F
from django.db.models.functions import TruncMonth
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.urls import reverse
from feriado.models import Feriado
from ferias.models import Ferias

from django.db.models import Q


class TipoReceitaManager(models.Manager):
    """Manager for the TipoReceita model."""

    def get_active(self):
        """
        Returns all active TipoReceita objects.
        """
        return self.filter(status="Ativo", registra_ponto="Sim")


class TipoReceita(models.Model):
    RECIBO_CHOICES = (
        ("Sim", "Sim"),
        ("Não", "Não"),
    )
    REGISTRA_PONTO_CHOICES = (
        ("Sim", "Sim"),
        ("Não", "Não"),
    )
    STATUS_CHOICES = (
        ("Ativo", "Ativo"),
        ("Inativo", "Inativo"),
    )
    id = models.IntegerField(primary_key=True)
    descricao = models.CharField(max_length=100)
    recibo = models.CharField(
        choices=RECIBO_CHOICES,
        default="Sim",
        max_length=3,
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        default="Ativo",
        max_length=10,
    )

    registra_ponto = models.CharField(
        choices=REGISTRA_PONTO_CHOICES,
        default="Sim",
        max_length=3,
    )

    objects = TipoReceitaManager()

    class Meta:
        """
        Metadata for the TipoReceita model.
        """

        ordering = ("descricao",)
        db_table = "tiporeceitas"
        verbose_name = "Tipo de Receita"
        verbose_name_plural = "Tipos de Receitas"

    def __str__(self):
        if self.status == "Ativo":
            return str(self.descricao)
        return f"{self.descricao} ({self.status})"


class PontoManager(models.Manager):
    """
    Manager for the Ponto model.
    """

    def for_day(self, day=None, user=None):
        """
        Returns all Ponto objects for a given day and user.
        Funciona dentro do relatório de +10 horas
        """
        if day is None:
            day = datetime.now().date()
        # start should be the day itself and the day before
        start = datetime.combine(day, time.min)  # - timedelta(days=1)
        end = datetime.combine(day, time.max)
        return self.filter(
            entrada__range=(start, end), usuario=user, over_10_hours_authorization=False
        )

    def for_day_resumo(self, day=None, user=None):
        """
        Returns all Ponto objects for a given day and user.
        Esse método funciona para o resumo (folha-ponto)
        """
        if day is None:
            day = datetime.now().date()
        # start should the day itself and the day before
        start = datetime.combine(day, time.min)  # - timedelta(days=1)
        # start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        return self.filter(entrada__range=(start, end),
                           usuario=user,
        )

    def for_month_resumo_cliente_tarefa(self, start_date=None, end_date=None, user=None, cliente=None, tarefa=None):
        """
        Returns all Ponto objects for a given day and user.
        Esse método funciona para o resumo (folha-ponto)
        """
        if start_date is None or end_date is None:
            # first day or the current date
            start_date = datetime.now().date().replace(day=1)
            # last day of the current month
            end_date = get_last_day_of_month(datetime.now().date())

        # start should the day itself and the day before
        start_date = datetime.combine(start_date, time.min)  # - timedelta(days=1)
        # start = datetime.combine(day, time.min)
        end_date = datetime.combine(end_date, time.max)
        return self.filter(entrada__range=(start_date, end_date),
                           usuario=user, cliente_id=cliente, tipo_receita=tarefa,
        )

    def for_day_unauthorized(self, day=None, user=None):
        """
        Returns all Ponto objects for a given day and user.
        Over 10 hours authorization is False
        """
        if day is None:
            day = datetime.now().date()
        # start should the day itself and the day before
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        return self.filter(
            entrada__range=(start, end), usuario=user, over_10_hours_authorization=False
        )

    def validate_over_10_hours(self, day=None, user=None):
        """Turn all over_10_hours_authorization to True  for a given day and user."""
        if day is None:
            day = datetime.now().date()
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        pontos = self.filter(
            entrada__range=(start, end), usuario=user, over_10_hours_authorization=False
        )
        for ponto in pontos:
            ponto.over_10_hours_authorization = True
            ponto.save()

    def for_range_days(self, start=None, end=None, user=None):
        """
        Returns all Ponto objects for a given range of days and user.
        """
        if start is None:
            start = datetime.now().date()
        if end is None:
            end = datetime.now().date()

        # turn start in datetime object
        start = datetime.strptime(start, "%Y-%m-%d")
        # turn end in datetime object
        end = datetime.strptime(end, "%Y-%m-%d")

        start = datetime.combine(start, time.min)
        end = datetime.combine(end, time.max)
        return self.filter(entrada__range=(start, end), usuario=user)

    def get_open_task_list(self):
        """
        Returns a dictionary with all open Ponto objects for all users.
        """
        open_task_list = []
        users = User.objects.all()
        for user in users:
            ponto = self.get_open_pontos_day_before(user).last()
            if ponto:
                open_task_list.append(
                    {
                        "user_id": user.id,
                        "username": user.username,
                        "ponto_id": ponto.id,
                        "entrada": ponto.entrada,
                    }
                )
        return open_task_list


    def get_open_pontos_day_before(self, user=None):
        """
        Returns all open Ponto objects for the day before.
        Template: apontamento/open_task_list.html
        """
        day = datetime.now().date() - timedelta(days=1)
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        return self.filter(
            entrada__range=(start, end),
            usuario=user,
            entrada__year__gte=2024,
            saida=None,
        )

    def get_open_pontos(self, user=None):
        """
        Returns all open Ponto objects for a given user.
        Template: core/home.html
        """
        return self.filter(
            usuario=user,
            entrada__year__gte=2024,
            saida=None,
        )

    def get_closed_pontos(self, user=None):
        """
        Returns all closed Ponto objects for a given user.
        """
        return self.filter(usuario=user, fechado=True)

    def total_day_time(self, day=None, user=None):
        """
        Returns the total time for a given day and user.
        """
        total = timedelta(0)
        for ponto in self.for_day(day, user):
            total += ponto.difference
        return total

    def total_day_time_resumo(self, day=None, user=None):
        """
        Returns the total time for a given day and user.
        """
        total = timedelta(0)
        for ponto in self.for_day_resumo(day, user):
            total += ponto.difference
        return total

    def total_range_days_time(self, start=None, end=None, user=None):
        """
        Returns the total time for a given range of days and user.
        """
        total_trabalhado = timedelta(hours=0)
        for ponto in self.for_range_days(start, end, user):
            total_trabalhado += ponto.difference
        return total_trabalhado

    def last_interaction(self, day=None, user=None):
        """
        Returns the last interaction for a given user.
        """
        if day is None:
            day = datetime.now().date()
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        return self.filter(entrada__range=(start, end), usuario=user).last()

    def get_last_open_task(self, user=None):
        """
        Returns the last open task for a given user.
        """
        return self.get_open_pontos(user).last()

    def get_total_hours_by_day_by_user(self, start, end, user):
        """
        Returns a list of dictionaries with day and the total hours, summarized by day worked for a given range of days and user.
        Using the format {day: date, total_hours: total_hours}.
        """
        total_hours = []
        credor = timedelta(hours=0)
        devedor = timedelta(hours=0)

        # turn start in datetime object
        start = datetime.strptime(start, "%Y-%m-%d")
        # turn end in datetime object
        end = datetime.strptime(end, "%Y-%m-%d")

        for day in range((end - start).days + 1):
            day = start + timedelta(days=day)
            horas_trabalhadas = self.total_day_time_resumo(day, user)

            feriado = Feriado.objects.is_holiday(
                year=day.year, month=day.month, day=day.day
            )

            if feriado:
                nome_feriado = Feriado.objects.get_description(
                    year=day.year, month=day.month, day=day.day
                )

            try:
                ferias = Ferias.objects.get_ferias(
                    data_inicial=day.date(),
                    data_final=day.date(),
                    user=user,
                )
            except ObjectDoesNotExist:
                ferias = "Não"

            if day.weekday() >= 5:
                carga_horaria = timedelta(hours=0)
            elif feriado:
                carga_horaria = timedelta(hours=0)
            elif ferias == "Sim":
                carga_horaria = timedelta(hours=0)
            else:
                user_carga_horaria = self.get_carga_horaria(user)
                carga_horaria = timedelta(hours=user_carga_horaria)

            if horas_trabalhadas > carga_horaria:
                credor = horas_trabalhadas - carga_horaria
                devedor = timedelta(hours=0)
            elif horas_trabalhadas <= carga_horaria:
                credor = timedelta(hours=0)
                devedor = carga_horaria - horas_trabalhadas

            total_hours.append(
                {
                    "day": day,
                    "user": user,
                    "username": User.objects.filter(username=user).first().username,
                    "total_hours": horas_trabalhadas,
                    "atrasado": self.get_status_atrasado(day, user),
                    "feriado": feriado,
                    "ferias": ferias,
                    "nome_feriado": nome_feriado if feriado else "",
                    "credor": credor,
                    "devedor": devedor,
                }
            )

        return total_hours



    def get_total_hours_by_month_by_user_cliente_tarefa(self, start, end, user, cliente=None, tarefa=None):
        """
        Returns a query with the worked hours by the user, cliente and tarefa.
        """


        # turn start in datetime object
        #start = datetime.strptime(start, "%Y-%m-%d")
        # turn end in datetime object
        # end = datetime.strptime(end, "%Y-%m-%d")

        query = Ponto.objects.filter(
            entrada__gte=start,
            saida__lte=end,
            usuario=user,
        )

        if cliente:
            query = query.filter(cliente_id=cliente)

        if tarefa:
            query = query.filter(tipo_receita=tarefa)


        return query



    def get_status_atrasado(self, day=None, user=None):
        """get the first entrada of the day and if it is later than 9:15, it is considered late"""
        if day is None:
            day = datetime.now().date()
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        ponto = self.filter(entrada__range=(start, end), usuario=user).first()
        feriado = Feriado.objects.is_holiday(
            year=day.year, month=day.month, day=day.day
        )
        if ponto:
            # check if ponto.entrada is a weekend
            if day.weekday() >= 5:
                return False

            if ponto.entrada.time() > time(9, 15) and not feriado:
                return True
            return False

    def get_credor_devedor(self, start, end, user=None):
        """return a dictionary with total_credor in hours and total_devedor in hours for a given range of days and user"""
        total_credor = timedelta(hours=0)
        total_devedor = timedelta(hours=0)

        # turn start in datetime object
        start = datetime.strptime(start, "%Y-%m-%d")
        # turn end in datetime object
        end = datetime.strptime(end, "%Y-%m-%d")

        for day in range((end - start).days + 1):
            day = start + timedelta(days=day)
            horas_trabalhadas = self.total_day_time_resumo(day, user)

            feriado = Feriado.objects.is_holiday(
                year=day.year, month=day.month, day=day.day
            )

            try:
                ferias = Ferias.objects.get_ferias(
                    data_inicial=day.date(),
                    data_final=day.date(),
                    user=user.id,
                )
            except ObjectDoesNotExist:
                ferias = "Não"

            if day.weekday() >= 5:
                # if it is a weekend
                carga_horaria = timedelta(hours=0)
            elif feriado:
                # if it is a holiday
                carga_horaria = timedelta(hours=0)
            elif ferias == "Sim":
                # if it is a vacation day
                carga_horaria = timedelta(hours=0)
            else:
                user_carga_horaria = self.get_carga_horaria(user)
                carga_horaria = timedelta(hours=user_carga_horaria)

            if horas_trabalhadas > carga_horaria:
                # if the user worked more than the regular hours
                total_credor += horas_trabalhadas - carga_horaria
            elif horas_trabalhadas < carga_horaria:
                # if the user worked less than the regular hours
                total_devedor += carga_horaria - horas_trabalhadas

        return {
            "total_credor": total_credor,
            "total_devedor": total_devedor,
        }

    def get_over_10_hours_list(self, user=None):
        """return a list of dictionaries with the days that the user worked more than 10 hours using the following format:
        {user: user, day: date, total_hours: total_hours}"""
        over_10_hours_list = []
        users = User.objects.filter(is_active=True)
        for day in range(30):
            day = datetime.now().date() - timedelta(days=day)
            # loop through users
            for user in users:

                horas_trabalhadas = self.total_day_time(day, user.id)
                if horas_trabalhadas > timedelta(hours=10):
                    over_10_hours_list.append(
                        {
                            "user_id": user.id,
                            "username": User.objects.get(id=user.id).username,
                            "day": day,
                            "total_hours": horas_trabalhadas,
                        }
                    )
        return over_10_hours_list

    def get_ajustes_autorizados(self):
        """return all ajustes authorized"""
        return self.filter(ajuste=True, status_ajuste=1)

    def get_ajustes_nao_autorizados(self):
        """return all ajustes denied"""
        return self.filter(ajuste=True, status_ajuste=2)

    def get_ajustes_pendentes(self):
        """return all ajustes pending"""
        return self.filter(ajuste=True, status_ajuste=0)

    def get_intervalo_30_minutos(self, user=None):
        # take all the points of those users who bateponto='Sim' and who have a point between 11 and 14
        # check if there is an interval between saida of one and entrada of the other
        # if there is an interval, check if it is greater than 30 minutes
        # if so, return the list of users and the days they worked without a 30 minute break
        intervalo_30_minutos = []
        users = User.objects.filter(userprofile__bateponto="Sim")
        for user in users:
            pontos = self.filter(usuario=user).order_by("entrada")
            for i in range(len(pontos) - 1):
                if pontos[i].get_intervalo:
                    intervalo = pontos[i + 1].entrada - pontos[i].saida
                    if intervalo < timedelta(minutes=30):
                        intervalo_30_minutos.append(
                            {
                                "user_id": user.id,
                                "username": user.username,
                                "day": pontos[i].entrada.date(),
                                "total_hours": intervalo,
                            }
                        )
        # sort intervalo_30_minutos by -id
        intervalo_30_minutos = sorted(intervalo_30_minutos, key=lambda x: x["day"], reverse=True)
        return intervalo_30_minutos

    def get_carga_horaria(self, user=None):
        """get UserProfile  carga horaria"""
        return User.objects.filter(username=user).first().userprofile.cargahoraria

    def get_automatically_closed_tasks(self):
        """Automatically close tasks are those with saida = 23:59:59"""
        return self.filter(entrada__year__gte=2024, saida__time=time(23, 59, 59))




class Ponto(models.Model):
    """
    Model to represent a point in time for a user.
    """

    id = models.IntegerField(primary_key=True, auto_created=True)
    entrada = models.DateTimeField()
    primeiro = models.BooleanField(default=False)
    segundo = models.BooleanField(default=False)
    atraso = models.BooleanField(default=False, verbose_name="Atraso")
    saida = models.DateTimeField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    fechado = models.BooleanField(default=False)
    cliente_id = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True
    )
    tipo_receita = models.ForeignKey(
        TipoReceita, on_delete=models.CASCADE, null=True, blank=True
    )
    atrasoautorizado = models.BooleanField(
        default=False, verbose_name="Atraso Autorizado"
    )
    over_10_hours_authorization = models.BooleanField(
        default=False, verbose_name="Autorização de +10 horas de jornada", db_index=True
    )
    ajuste = models.BooleanField(default=False, db_index=True, verbose_name="Ajuste")

    # Define choices for ajuste_autorizado
    PENDENTE = 0
    AUTORIZADO = 1
    NEGADO = 2

    AJUSTE_STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (AUTORIZADO, 'Autorizado'),
        (NEGADO, 'Negado'),
    ]

    status_ajuste = models.PositiveSmallIntegerField(
        choices=AJUSTE_STATUS_CHOICES,
        default=PENDENTE,
        db_index=True,
        verbose_name="Status do Ajuste"
    )

    ajuste_autorizado = models.BooleanField(
        default=False, db_index=True, verbose_name="Ajuste Autorizado"
    )


    objects = PontoManager()

    class Meta:
        """
        Metadata for the Ponto model.
        """

        ordering = ("entrada",)
        db_table = "pontos"
        verbose_name = "Ponto"
        verbose_name_plural = "Pontos"

    @property
    def difference(self):
        """
        Calculates the difference between the entry and exit times.
        """
        if self.saida is not None:
            return self.saida - self.entrada

        diff = datetime.now() - self.entrada
        seconds = round(diff.total_seconds())
        return timedelta(seconds=seconds)

    @property
    def allow_update(self):
        """
        Returns True if the Ponto object can be updated.
        """
        current_date = datetime.now().date()
        diff_days = current_date - self.entrada.date()

        if diff_days.days <= 3 and current_date.weekday() == 0:
            # Allow update if the difference between the current date
            # and the date of the Ponto object is less than 3 days AND
            # if the current date is Monday.
            return True

        if diff_days.days <= 1:
            # Allow update if the difference between the current date
            # and the date of the Ponto object is less than 1 day.
            return True
        else:
            return False

    def __str__(self) -> str:
        """
        Returns a string representation of the Ponto object.
        """
        return f"{self.usuario} {self.entrada} {self.saida} {self.difference}"

    @property
    def cliente(self):
        """
        Returns the client for the Ponto object.
        """
        if self.cliente_id is not None:
            return self.cliente_id
        return "-"

    @property
    def get_intervalo(self):
        """check if saida betweem 11 and 14"""
        if self.saida:
            if self.saida.time() > time(11, 0) and self.saida.time() < time(13, minute=59):
                return True
            return False
        return False

    def get_absolute_url(self):
        """Returns the url to access a particular instance of the model."""
        return reverse("apontamento:appointment_detail", args=[self.pk])
