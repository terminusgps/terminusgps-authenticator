from django.dispatch import receiver
from django.db.models.signals import post_save

from terminusgps_timekeeper.models import Employee, EmployeePunchCard


@receiver(post_save, sender=Employee)
def create_punch_card(sender, instance, created, raw, using, update_fields, **kwargs):
    if not EmployeePunchCard.objects.filter(employee=instance).exists():
        EmployeePunchCard.objects.create(employee=instance)
