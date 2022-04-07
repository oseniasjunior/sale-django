from celery import shared_task
from basic import actions


@shared_task(queue='default')
def sale_by_year():
    actions.SaleActions.sale_by_year()
