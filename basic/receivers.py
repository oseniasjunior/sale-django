from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from basic import models


@receiver(post_save, sender=models.State, dispatch_uid='create_file_state', weak=False)
def create_file_state(instance, **kwargs):
    with open('states.txt', 'a') as file:
        file.write(f'{instance.id}|{instance.name}')


@receiver(pre_save, sender=models.SaleItem, dispatch_uid='update_sale_item_price', weak=False)
def update_sale_item_price(instance, **kwargs):
    instance.price = instance.product.sale_price
