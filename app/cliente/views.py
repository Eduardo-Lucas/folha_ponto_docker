import json

from django.db.models import Q
from django.http import HttpResponse

from .models import Cliente


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
