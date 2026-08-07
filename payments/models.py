from django.db import models
from members.models import Member

class Contribution(models.Model):
    start_date=models.DateField()

    end_date=models.DateField(
        null=True,
        blank=True
    )
    amount_required= models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
def __str__(self):
    return f"{self.start_date} -  {self.amount_required} TZS"


class Payment(models.Model):
    member=models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )
    payment_date=models.DateField()

    amount_paid=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    reference_number=models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    note=models.TextField(
        blank=True,
        null=True
    )
def __str__(self):
    return f"{self.member} - {self.amount_paid} TZS"  

class PaymentAllocation(models.Model):
    payment=models.ForeignKey(
        Payment,
        on_delete=models. CASCADE,
        related_name="allocations"
    )

    contribution_month=models.PositiveSmallIntegerField()
    contribution_year=models.PositiveIntegerField()
    amount_allocated=models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    class Meta:
        ordering =[
            "contribution_year",
            "contribution_month",
        ]

    def __str__(self):
        return(
            f"{self.payment.member.member_number} -"
            f"{self.contribution_month}/{self.contribution_year} -"
            f"{self.amount_allocated}"
        )
