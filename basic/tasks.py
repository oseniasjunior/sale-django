from celery import shared_task
from basic import actions
from django.utils.timezone import now


@shared_task(queue='default')
def sale_by_year():
    actions.SaleActions.sale_by_year()


@shared_task(queue='periodic')
def periodic_task():
    print(f'Executou em {now()}')
