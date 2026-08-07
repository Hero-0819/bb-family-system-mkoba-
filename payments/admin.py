from django.contrib import admin
from .models import (
    Contribution,
    Payment,
    PaymentAllocation,
)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "payment_date",
        "amount_paid",
        "reference_number",
    )

    search_fields = (
        "member__member_number",
        "member__first_name",
        "member__last_name",
        "reference_number",
    )

    list_filter = (
        "payment_date",
    )

    ordering = (
        "payment_date",
    )


admin.site.register(Contribution)
admin.site.register(PaymentAllocation)