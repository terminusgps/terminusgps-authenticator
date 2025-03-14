from django.contrib import admin

from terminusgps_authenticator.models import Employee, EmployeePunchCard, EmployeeShift


@admin.register(EmployeeShift)
class EmployeeShiftAdmin(admin.ModelAdmin):
    list_display = ["employee", "start_datetime", "end_datetime", "duration"]
    readonly_fields = ["employee", "duration"]
    list_filter = ["employee", "start_datetime", "end_datetime"]


@admin.register(EmployeePunchCard)
class EmployeePunchCardAdmin(admin.ModelAdmin):
    list_display = ["employee", "punched_in"]
    actions = ["punch_employees_in", "punch_employees_out"]

    @admin.action(description="Punch selected employees in")
    def punch_employees_in(self, request, queryset) -> None:
        return

    @admin.action(description="Punch selected employees in")
    def punch_employees_out(self, request, queryset) -> None:
        return


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["user", "phone", "title", "pfp"]}),
        ("Read-only", {"fields": ["code"]}),
    ]
    readonly_fields = ["code"]
