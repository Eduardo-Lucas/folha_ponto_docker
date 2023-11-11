from django.urls import path
from .views import AppointmentListView, apontamento_list, folha_ponto

app_name = "apontamento"

urlpatterns = [
    path("apontamento-list", apontamento_list, name="apontamento-list"),
    path("folha-ponto", folha_ponto, name="folha-ponto"),
    path('appointment-list/', AppointmentListView.as_view(), name='appointment_list'),

]
