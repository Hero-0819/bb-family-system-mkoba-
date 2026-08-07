from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment
from .services import allocate_payment

@receiver(post_save, sender=Payment)

def payment_saved(sender , instance ,created , **kwargs):
    print("signal called")

    if created:
        print("allocation starting")
        allocate_payment(instance)
