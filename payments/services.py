from datetime import date
from config.constants import SYSTEM_START_DATE
from django.db.models import Q ,Sum
from .models import PaymentAllocation, Contribution
from _decimal import Decimal
import calendar

def get_required_amount(year, month):
    first_day = date(year, month, 1)

    rule = Contribution.objects.filter(
        start_date__lte=first_day
    ).filter(
        Q(end_date__gte=first_day) | Q(end_date__isnull=True)
    ).first()

    if rule:
        return Decimal(rule.amount_required)

    return Decimal("0")

def get_allocated_amount(member, year , month):
    total= (
        PaymentAllocation.objects.filter(
            payment__member=member,
            contribution_year=year,
            contribution_month=month,
        ).aggregate(
            total=Sum("amount_allocated")
        )
    )
    return total ["total"] or Decimal("0")

def  next_month(year , month):
    if month ==12:
        return year + 1,1
    
    return year , month + 1

def allocate_payment(payment):

    member = payment.member
    remaining = Decimal(payment.amount_paid)

    print("MEMBER:", member.member_number)
    print("PAYMENT:", remaining)

    # Kila payment inaanzia November 2024
    year = SYSTEM_START_DATE.year
    month = SYSTEM_START_DATE.month

    print("START:", year, month)

    # Usiruhusu allocation kwenda future
    today = date.today()

    months_checked = 0
    max_months = 100

    while remaining > 0 and months_checked < max_months:

        # Stop if we have reached a future month
        if (year, month) > (today.year, today.month):
            print("REACHED FUTURE MONTH")
            break

        print("CHECKING MONTH:", year, month)

        required = get_required_amount(year, month)

        print("REQUIRED:", required)

        allocated = get_allocated_amount(
            member,
            year,
            month
        )

        print("ALREADY ALLOCATED:", allocated)

        still_needed = required - allocated

        print("STILL NEEDED:", still_needed)

        # Hakuna contribution rule
        if required <= 0:

            print("NO RULE FOUND")

            year, month = next_month(
                year,
                month
            )

            months_checked += 1

            continue

        # Mwezi umeshakamilika
        if still_needed <= 0:

            print("MONTH COMPLETE")

            year, month = next_month(
                year,
                month
            )

            months_checked += 1

            continue

        # Tumia payment kulipa deni la mwezi huu
        allocated_amount = min(
            remaining,
            still_needed
        )

        print(
            "CREATING ALLOCATION:",
            allocated_amount
        )

        PaymentAllocation.objects.create(
            payment=payment,
            contribution_month=month,
            contribution_year=year,
            amount_allocated=allocated_amount,
        )

        remaining -= allocated_amount

        print("REMAINING:", remaining)

        # Endelea mwezi unaofuata
        year, month = next_month(
            year,
            month
        )

        months_checked += 1

    if remaining > 0:

        print(
            "WARNING: Payment could not be fully allocated.",
            "Remaining:",
            remaining
        )

def get_total_paid(member):
    total = PaymentAllocation.objects.filter(
        payment__member=member
    ).aggregate(
        total=Sum("amount_allocated")
    )

    return total["total"] or Decimal("0")


def get_total_required():
    today = date.today()
    year = SYSTEM_START_DATE.year
    month = SYSTEM_START_DATE.month

    total = 0

    
    while (year, month) <= (today.year, today.month):
        total += get_required_amount(year, month)
        year, month = next_month(year, month)

    return total


def get_member_status(member):

    required = get_total_required()

    paid = get_total_paid(member)

    balance = required - paid

    if balance < 0:
        balance = 0


    # Contribution progress
    if required > 0:

        percentage = (paid / required) * 100

    else:

        percentage = 0


    if percentage > 100:
        percentage = 100


    # Monthly statement
    statement = get_member_statement(member)


    # Count months with outstanding balance
    unpaid_months = 0

    for item in statement:

        if item["balance"] > 0:

            unpaid_months += 1


    # Membership status
    if unpaid_months > 3:

        membership_status = "INACTIVE"

    elif unpaid_months >= 2:

        membership_status = "WARNING"

    else:

        membership_status = "ACTIVE"


    # Membership message
    if membership_status == "ACTIVE":

        membership_message = (
            "Uanachama wako uko katika hali nzuri. "
            "Endelea kuchangia kwa wakati."
        )

    elif membership_status == "WARNING":

        membership_message = (
            f"Una madeni ya miezi {unpaid_months}. "
            "Tafadhali kamilisha michango yako "
            "ili uendelee kuwa katika hali nzuri."
        )

    else:

        membership_message = (
            f"Uanachama wako uko INACTIVE kwa sababu "
            f"una madeni ya miezi {unpaid_months}. "
            "Tafadhali lipa madeni yako hadi mwezi husika "
            "ili kurejesha hali yako kuwa ACTIVE."
        )


    # Current month
    today = date.today()

    current_month = calendar.month_name[today.month]

    current_year = today.year


    # Find current month information
    current_month_required = 0

    current_month_paid = 0

    current_month_balance = 0

    current_month_status = "Unpaid"


    for item in statement:

        if (
            item["year"] == current_year
            and item["month"] == current_month
        ):

            current_month_required = item["required"]

            current_month_paid = item["paid"]

            current_month_balance = item["balance"]

            current_month_status = item["status"]

            break


    # Current month message
    if current_month_balance > 0:

        current_month_message = (
            f"Una deni la TZS {current_month_balance:,} "
            f"kwa mwezi wa {current_month} {current_year}."
        )

    else:

        current_month_message = (
            f"Umefanikisha mchango wa "
            f"{current_month} {current_year}."
        )


    return {

        "required": required,

        "paid": paid,

        "balance": balance,

        "percentage": round(percentage, 1),

        "unpaid_months": unpaid_months,

        "membership_status": membership_status,

        "membership_message": membership_message,

        "current_month": current_month,

        "current_year": current_year,

        "current_month_required": current_month_required,

        "current_month_paid": current_month_paid,

        "current_month_balance": current_month_balance,

        "current_month_status": current_month_status,

        "current_month_message": current_month_message,

        "status": (
            "Complete"
            if balance == 0
            else "Outstanding"
        ),

    }

def get_member_statement(member):

    today = date.today()

    year = SYSTEM_START_DATE.year
    month = SYSTEM_START_DATE.month

    statement = []

    while (year, month) <= (today.year, today.month):

        required = get_required_amount(year, month)

        paid = get_allocated_amount(
            member,
            year,
            month
        )

        balance = required - paid

        # Determine monthly status
        if paid >= required and required > 0:

            status = "Paid"

        elif paid > 0:

            status = "Partial"

        else:

            status = "Unpaid"


        statement.append({

            "month": calendar.month_name[month],

            "year": year,

            "required": required,

            "paid": paid,

            "balance": max(balance, 0),

            "status": status,

        })


        year, month = next_month(
            year,
            month
        )


    return statement
