from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext

from terminusgps_authenticator.models import (
    AuthenticatorEmployee,
    AuthenticatorLogItem,
    AuthenticatorLogReport,
    AuthenticatorEmployeeShift,
)


@admin.register(AuthenticatorEmployee)
class AuthenticatorEmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "phone", "title", "pfp", "punched_in"]}),
        ("Read-only", {"fields": ["code"]}),
    ]
    readonly_fields = ["code"]
    actions = ["set_employee_punched_in", "set_employee_punched_out"]
    list_filter = ["user__username", "punched_in"]
    list_display = ["user", "phone", "punched_in"]

    @admin.action(description="Set employee as punched in")
    def set_employee_punched_in(self, request, queryset):
        results = {"success": [], "skipped": []}
        for employee in queryset:
            if employee.punched_in:
                results["skipped"].append(employee)
                continue
            employee.punched_in = True
            employee.save()
            results["success"].append(employee)

        if results["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched in.",
                    "%(count)s employees were already punched in.",
                    len(results["skipped"]),
                )
                % {"count": len(results["skipped"])},
                messages.WARNING,
            )
        if results["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched in.",
                    "%(count)s employees were punched in.",
                    len(results["success"]),
                )
                % {"count": len(results["success"])},
                messages.SUCCESS,
            )

    @admin.action(description="Set employee as punched out")
    def set_employee_punched_out(self, request, queryset):
        results = {"success": [], "skipped": []}
        for employee in queryset:
            if not employee.punched_in:
                results["skipped"].append(employee)
                continue
            employee.punched_in = False
            employee.save()
            results["success"].append(employee)

        if results["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched out.",
                    "%(count)s employees were already punched out.",
                    len(results["skipped"]),
                )
                % {"count": len(results["skipped"])},
                messages.WARNING,
            )
        if results["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched out.",
                    "%(count)s employees were punched out.",
                    len(results["success"]),
                )
                % {"count": len(results["success"])},
                messages.SUCCESS,
            )


@admin.register(AuthenticatorLogItem)
class AuthenticatorLogItemAdmin(admin.ModelAdmin):
    list_display = ["employee", "action", "datetime"]
    readonly_fields = ["employee", "action", "datetime"]
    list_filter = ["employee", "action", "datetime"]


@admin.register(AuthenticatorLogReport)
class AuthenticatorLogReportAdmin(admin.ModelAdmin):
    list_display = ["user", "datetime"]
    fields = ["datetime", "user", "pdf", "logs"]
    actions = ["generate_employee_shifts", "generate_pdf_file"]
    list_filter = ["user", "datetime"]

    @admin.action(description="Generate pdf file")
    def generate_pdf_file(self, request, queryset):
        results = {"success": [], "failure": [], "skipped": []}

        for report in queryset:
            if report.pdf:
                results["skipped"].append(report)
                continue
            try:
                report.generate_pdf()
                results["success"].append(report)
            except (AssertionError, ValueError):
                results["failure"].append(report)

        if results["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report generated a pdf file.",
                    "%(count)s reports generated pdf files.",
                    len(results["success"]),
                )
                % {"count": len(results["success"])},
                messages.SUCCESS,
            )
        if results["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report already generated a pdf file and was skipped.",
                    "%(count)s reports already generated pdf files and were skipped.",
                    len(results["skipped"]),
                )
                % {"count": len(results["skipped"])},
                messages.WARNING,
            )
        if results["failure"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report failed to generate a pdf file.",
                    "%(count)s reports failed to generate pdf files.",
                    len(results["failure"]),
                )
                % {"count": len(results["failure"])},
                messages.ERROR,
            )

    @admin.action(description="Generate employee shifts")
    def generate_employee_shifts(self, request, queryset):
        results = {"success": [], "failure": [], "skipped": []}

        for report in queryset:
            if report.shifts_generated:
                results["skipped"].append(report)
                continue
            try:
                report.generate_shifts()
                results["success"].append(report)
            except AssertionError:
                results["failure"].append(report)

        if results["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report had shifts generated.",
                    "%(count)s reports had shifts generated.",
                    len(results["success"]),
                )
                % {"count": len(results["success"])},
                messages.SUCCESS,
            )
        if results["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report already generated shifts and was skipped.",
                    "%(count)s reports already generated shifts and were skipped.",
                    len(results["skipped"]),
                )
                % {"count": len(results["skipped"])},
                messages.WARNING,
            )
        if results["failure"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s report failed to generate shifts.",
                    "%(count)s reports failed to generate shifts.",
                    len(results["failure"]),
                )
                % {"count": len(results["failure"])},
                messages.ERROR,
            )


@admin.register(AuthenticatorEmployeeShift)
class AuthenticatorEmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ["employee", "start_datetime", "end_datetime", "duration"]
    readonly_fields = ["employee", "duration", "report"]
    list_filter = ["employee", "start_datetime", "end_datetime"]
