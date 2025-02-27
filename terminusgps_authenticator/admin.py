from django.contrib import admin

from terminusgps_authenticator.models import AuthenticatorEmployee, AuthenticatorLogItem


@admin.register(AuthenticatorEmployee)
class AuthenticatorEmployeeAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    list_display_links = ["user"]
    fields = ["user", "code", "pstate"]
    readonly_fields = ["code"]


@admin.register(AuthenticatorLogItem)
class AuthenticatorLogItemAdmin(admin.ModelAdmin):
    list_display = ["datetime", "employee", "pstate"]
