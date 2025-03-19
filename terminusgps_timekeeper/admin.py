from django.contrib import admin, messages
from django.utils.translation import ngettext

from terminusgps_timekeeper.models import (
    Employee,
    EmployeePunchCard,
    EmployeeShift,
    Report,
)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["id", "start_date", "end_date"]
    list_filter = ["start_date", "end_date"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "phone", "title", "pfp"]}),
        ("Read-only", {"fields": ["code"]}),
    ]
    readonly_fields = ["code"]
    actions = ["punch_employees_in", "punch_employees_out"]

    @admin.action(description="Punch selected employees in")
    def punch_employees_in(self, request, queryset) -> None:
        results_map = {"success": [], "skipped": []}
        for employee in queryset:
            if employee.punch_card.punched_in:
                results_map["skipped"].append(employee.punch_card)
                continue

            employee.punch_card.punched_in = True
            employee.punch_card.save()
            results_map["success"].append(employee.punch_card)

        if results_map["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched in and was skipped.",
                    "%(count)s employees were already punched in and were skipped.",
                    len(results_map["skipped"]),
                )
                % {"count": len(results_map["skipped"])},
                messages.WARNING,
            )
        if results_map["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched in.",
                    "%(count)s employees were punched in.",
                    len(results_map["success"]),
                )
                % {"count": len(results_map["success"])},
                messages.SUCCESS,
            )

    @admin.action(description="Punch selected employees out")
    def punch_employees_out(self, request, queryset) -> None:
        results_map = {"success": [], "skipped": []}
        for employee in queryset:
            if not employee.punch_card.punched_in:
                results_map["skipped"].append(employee.punch_card)
                continue

            employee.punch_card.punched_in = False
            employee.punch_card.save()
            results_map["success"].append(employee.punch_card)

        if results_map["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched out and was skipped.",
                    "%(count)s employees were already punched out and were skipped.",
                    len(results_map["skipped"]),
                )
                % {"count": len(results_map["skipped"])},
                messages.WARNING,
            )
        if results_map["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched out.",
                    "%(count)s employees were punched out.",
                    len(results_map["success"]),
                )
                % {"count": len(results_map["success"])},
                messages.SUCCESS,
            )


@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ["employee", "end_datetime", "duration"]
    list_filter = ["employee", "end_datetime"]
    readonly_fields = ["employee", "duration", "start_datetime", "end_datetime"]


@admin.register(EmployeePunchCard)
class EmployeePunchCardAdmin(admin.ModelAdmin):
    list_display = ["employee", "punched_in"]
    fieldsets = [
        (None, {"fields": ["punched_in"]}),
        (
            "Read-only",
            {"fields": ["employee", "last_punch_in_time", "_prev_punch_state"]},
        ),
    ]
    actions = ["punch_employees_in", "punch_employees_out"]
    readonly_fields = ["employee", "last_punch_in_time", "_prev_punch_state"]

    @admin.action(description="Punch selected employees in")
    def punch_employees_in(self, request, queryset) -> None:
        results_map = {"success": [], "skipped": []}
        for pcard in queryset:
            if pcard.punched_in:
                results_map["skipped"].append(pcard)
                continue

            pcard.punched_in = True
            pcard.save()
            results_map["success"].append(pcard)

        if results_map["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched in and was skipped.",
                    "%(count)s employees were already punched in and were skipped.",
                    len(results_map["skipped"]),
                )
                % {"count": len(results_map["skipped"])},
                messages.WARNING,
            )
        if results_map["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched in.",
                    "%(count)s employees were punched in.",
                    len(results_map["success"]),
                )
                % {"count": len(results_map["success"])},
                messages.SUCCESS,
            )

    @admin.action(description="Punch selected employees out")
    def punch_employees_out(self, request, queryset) -> None:
        results_map = {"success": [], "skipped": []}
        for pcard in queryset:
            if not pcard.punched_in:
                results_map["skipped"].append(pcard)
                continue

            pcard.punched_in = False
            pcard.save()
            results_map["success"].append(pcard)

        if results_map["skipped"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was already punched out and was skipped.",
                    "%(count)s employees were already punched out and were skipped.",
                    len(results_map["skipped"]),
                )
                % {"count": len(results_map["skipped"])},
                messages.WARNING,
            )
        if results_map["success"]:
            self.message_user(
                request,
                ngettext(
                    "%(count)s employee was punched out.",
                    "%(count)s employees were punched out.",
                    len(results_map["success"]),
                )
                % {"count": len(results_map["success"])},
                messages.SUCCESS,
            )
