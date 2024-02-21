from celery import shared_task

from apontamento.models import Ponto

@shared_task
def close_open_tasks():
    """Close the open tasks."""
    # Check if there are open tasks
    pontos = Ponto.objects.get_open_task_list()
    if pontos:
        # call fecha_tarefa
        for ponto in pontos:
            ponto.fecha_tarefa(ponto.ponto_id)
