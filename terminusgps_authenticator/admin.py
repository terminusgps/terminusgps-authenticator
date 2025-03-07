from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from terminusgps_authenticator.models import AuthenticatorEmployee, AuthenticatorLogItem


@admin.register(AuthenticatorEmployee)
class AuthenticatorEmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "phone", "title", "pfp", "punched_in"]}),
        ("Read-only", {"fields": ["code"]}),
    ]
    readonly_fields = ["code"]
    actions = ["set_employee_punched_in", "set_employee_punched_out"]

    @admin.action(description="Set employee as punched in")
    def set_employee_punched_in(self, request, queryset):
        for employee in queryset:
            employee.punched_in = True
            employee.save()

        self.message_user(
            request,
            ngettext(
                "%(count)s employee was punched in.",
                "%(count)s employees were punched in.",
                len(queryset),
            )
            % {"count": len(queryset)},
            messages.SUCCESS,
        )

    @admin.action(description="Set employee as punched out")
    def set_employee_punched_out(self, request, queryset):
        for employee in queryset:
            employee.punched_in = False
            employee.save()

        self.message_user(
            request,
            ngettext(
                "%(count)s employee was punched out.",
                "%(count)s employees were punched out.",
                len(queryset),
            )
            % {"count": len(queryset)},
            messages.SUCCESS,
        )


@admin.register(AuthenticatorLogItem)
class AuthenticatorLogItemAdmin(admin.ModelAdmin):
    list_display = ["employee", "action", "datetime"]
    readonly_fields = ["employee", "action", "datetime"]
