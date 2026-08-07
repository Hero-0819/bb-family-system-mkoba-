from datetime import date

from members.models import Member
from payments.models import Contribution


def create_monthly_contributions(year, month):

    members = Member.objects.all()


    for member in members:

        exists = Contribution.objects.filter(
            member=member,
            year=year,
            month=month
        ).exists()


        if not exists:

            Contribution.objects.create(

                member=member,

                year=year,

                month=month

            )
            