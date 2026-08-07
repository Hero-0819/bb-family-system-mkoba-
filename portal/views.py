from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum

from members.models import Member
from payments.models import Payment
from payments.services import get_member_status, get_member_statement


@staff_member_required
def admin_dashboard(request):
    members = Member.objects.all()

    total_members = members.count()

    active_members = 0
    warning_members = 0
    inactive_members = 0

    outstanding_members = []

    # Check every member's status
    for member in members:
        status = get_member_status(member)

        if status["membership_status"] == "ACTIVE":
            active_members += 1
        elif status["membership_status"] == "WARNING":
            warning_members += 1
        elif status["membership_status"] == "INACTIVE":
            inactive_members += 1

        # Add members who have outstanding balance
        if status["balance"] > 0:
            outstanding_members.append({
                "member": member,
                "paid": status["paid"],
                "balance": status["balance"],
                "membership_status": status["membership_status"],
                "unpaid_months": status["unpaid_months"],
            })

    # Sort members by highest debt first
    outstanding_members.sort(
        key=lambda x: x["balance"],
        reverse=True
    )

    # Total amount paid by all members
    total_paid = (
        Payment.objects.aggregate(
            total=Sum("amount_paid")
        )["total"] or 0
    )

    # Latest 10 payments
    recent_payments = (
        Payment.objects
        .select_related("member")
        .order_by("-payment_date", "-id")[:10]
    )

    context = {
        "total_members": total_members,
        "active_members": active_members,
        "warning_members": warning_members,
        "inactive_members": inactive_members,
        "total_paid": total_paid,
        "recent_payments": recent_payments,
        "outstanding_members": outstanding_members,
    }

    return render(
        request,
        "portal/admin_dashboard.html",
        context
    )


def home(request):
    if request.method == "POST":
        member_number = request.POST.get("member_number")
        phone_number = request.POST.get("phone_number")

        try:
            member = Member.objects.get(
                member_number=member_number,
                phone=phone_number
            )

            return redirect(
                "dashboard",
                member_id=member.id
            )

        except Member.DoesNotExist:
            messages.error(
                request,
                "Member Number au Phone Number si sahihi"
            )

    return render(
        request,
        "portal/home.html"
    )


def dashboard(request, member_id):
    member = get_object_or_404(
        Member,
        id=member_id
    )

    status = get_member_status(member)
    statement = get_member_statement(member)

    context = {
        "member": member,
        "status": status,
        "statement": statement,
    }

    return render(
        request,
        "portal/dashboard.html",
        context
    )

