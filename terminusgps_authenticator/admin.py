from django.contrib import admin

from terminusgps_authenticator.models import AuthenticatorEmployee, AuthenticatorLogItem


@admin.register(AuthenticatorEmployee)
class AuthenticatorEmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "title", "pfp"]}),
        ("Read-only", {"fields": ["code", "_punched_in"]}),
    ]
    readonly_fields = ["code", "_punched_in"]


@admin.register(AuthenticatorLogItem)
class AuthenticatorLogItemAdmin(admin.ModelAdmin):
    list_display = ["employee", "action", "datetime"]
    readonly_fields = ["employee", "action", "datetime"]
