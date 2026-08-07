from django.db import models

class Member(models.Model):
    member_number=models.CharField(
        max_length=10,
        unique=True
    )

    first_name=models.CharField(
        max_length=50
    )

    last_name=models.CharField(
        max_length=50
    )
    phone=models.CharField(
        max_length=15
    )

    join_date=models.DateField()

    contribution_start_date=models.DateField(
        help_text="Date from which member contribution should be calculated "
    )

    is_active= models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.member_number}         {self.first_name}          {self.last_name}"



    