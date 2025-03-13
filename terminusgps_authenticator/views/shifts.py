from typing import Any

from django.views.generic import (
    ArchiveIndexView,
    YearArchiveView,
    MonthArchiveView,
    DayArchiveView,
    WeekArchiveView,
)

from terminusgps_authenticator.models import EmployeeShift
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


class ShiftArchiveIndexView(ArchiveIndexView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/shifts/archives/index.html"
    partial_template_name = (
        "terminusgps_authenticator/shifts/archives/partials/_index.html"
    )
    model = EmployeeShift
    allow_empty = True
    allow_future = False
    content_type = "text/html"
    date_field = "end_datetime"
    ordering = "-end_datetime"
    paginate_by = 15


class ShiftYearArchiveView(YearArchiveView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/shifts/archives/year.html"
    partial_template_name = (
        "terminusgps_authenticator/shifts/archives/partials/_year.html"
    )
    model = EmployeeShift
    allow_empty = True
    allow_future = False
    content_type = "text/html"
    date_field = "end_datetime"
    ordering = "-end_datetime"
    paginate_by = 15

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = f"Shifts in {self.get_year()}"
        return context


class ShiftMonthArchiveView(MonthArchiveView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/shifts/archives/month.html"
    partial_template_name = (
        "terminusgps_authenticator/shifts/archives/partials/_month.html"
    )
    model = EmployeeShift
    allow_empty = True
    allow_future = False
    content_type = "text/html"
    date_field = "end_datetime"
    ordering = "-end_datetime"
    paginate_by = 15

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = f"Shifts on {self.get_month()} {self.get_year()}"
        return context


class ShiftDayArchiveView(DayArchiveView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/shifts/archives/day.html"
    partial_template_name = (
        "terminusgps_authenticator/shifts/archives/partials/_day.html"
    )
    model = EmployeeShift
    allow_empty = True
    allow_future = False
    content_type = "text/html"
    date_field = "end_datetime"
    ordering = "-end_datetime"
    paginate_by = 15

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = (
            f"Shifts on {self.get_month()} {self.get_day()}, {self.get_year()}"
        )
        return context


class ShiftWeekArchiveView(WeekArchiveView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/shifts/archives/week.html"
    partial_template_name = (
        "terminusgps_authenticator/shifts/archives/partials/_week.html"
    )
    model = EmployeeShift
    allow_empty = True
    allow_future = False
    content_type = "text/html"
    date_field = "end_datetime"
    ordering = "-end_datetime"
    paginate_by = 15
