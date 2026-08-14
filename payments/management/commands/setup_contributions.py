from django.core.management.base import BaseCommand
from datetime import date
from payments.models import Contribution


class Command(BaseCommand):

    help = "Create or update BB Family contribution rules"

    def handle(self, *args, **options):

        Contribution.objects.update_or_create(
            start_date=date(2024, 11, 1),
            defaults={
                "end_date": date(2026, 2, 28),
                "amount_required": 3000,
            },
        )

        Contribution.objects.update_or_create(
            start_date=date(2026, 3, 1),
            defaults={
                "end_date": None,
                "amount_required": 5000,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Contribution rules successfully configured."
            )
        )
