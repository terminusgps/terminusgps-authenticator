from typing import Any
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views.generic import ListView

from terminusgps_timekeeper.models import Employee, EmployeeShift
from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin


class ShiftListView(ListView, LoginRequiredMixin, HtmxTemplateResponseMixin):
    model = EmployeeShift
    template_name = "terminusgps_timekeeper/shifts/list.html"
    partial_template_name = "terminusgps_timekeeper/shifts/partials/_list.html"
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    permission_denied_message = "Please login and try again."
    raise_exception = False
    paginate_by = 15
    ordering = "-end_datetime"

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        try:
            self.employee = Employee.objects.get(pk=self.kwargs["pk"])
        except Employee.DoesNotExist:
            self.employee = None

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["employee"] = self.employee
        context["title"] = f"{self.employee}'s Shifts"
        return context

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if self.employee is not None:
            qs = qs.filter(employee=self.employee)
        return qs
