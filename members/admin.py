from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        "member_number",
        "first_name",
        "last_name",
        "phone",
        "join_date",
        "contribution_start_date",
        "is_active",
    )
    search_fields = (
        "member_number",
        "first_name",
        "last_name",
        "phone",
    )
    list_filter = (
        "is_active",
        "join_date",
    )
    ordering = (
        "member_number",
    )
