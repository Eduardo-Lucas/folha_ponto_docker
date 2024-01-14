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
            clientes = Cliente.objects.filter(Q(codigosistema=int(query)))
        else:
            clientes = Cliente.objects.filter(Q(nomerazao__icontains=query))

        results = []
        for cliente in clientes:
            place_json = cliente.nomerazao
            results.append(place_json)
        data = json.dumps(results)
    mimetype = "application/json"
    return HttpResponse(data, mimetype)
