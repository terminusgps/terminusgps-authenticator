from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.views.generic import (
    ArchiveIndexView,
    DayArchiveView,
    DetailView,
    MonthArchiveView,
    YearArchiveView,
)

from terminusgps_authenticator.models import AuthenticatorLogItem
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


class EmployeeLogIndexView(
    LoginRequiredMixin, HtmxTemplateResponseMixin, ArchiveIndexView
):
    allow_empty = True
    date_field = "datetime"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    ordering = "-datetime"
    paginate_by = 5
    partial_template_name = (
        "terminusgps_authenticator/logs/partials/_employee_index.html"
    )
    template_name = "terminusgps_authenticator/logs/employee_index.html"
    login_url = reverse_lazy("login")
    permission_denied_message = "Please login and try again."
    raise_exception = False

    def get_queryset(self) -> QuerySet:
        qs: QuerySet = super().get_queryset()
        pk: int = self.kwargs["pk"]
        return qs.filter(employee__pk=pk)


class LogDetailView(HtmxTemplateResponseMixin, DetailView):
    extra_context = {"title": "Inspect Log"}
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    template_name = "terminusgps_authenticator/logs/detail.html"
    partial_template_name = "terminusgps_authenticator/logs/partials/_detail.html"
    context_object_name = "log"


class LogArchiveIndexView(HtmxTemplateResponseMixin, ArchiveIndexView):
    allow_empty = True
    date_field = "datetime"
    extra_context = {"title": "Logs"}
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    ordering = "-datetime"
    paginate_by = 15
    partial_template_name = "terminusgps_authenticator/logs/partials/_index.html"
    template_name = "terminusgps_authenticator/logs/index.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs


class LogArchiveYearView(HtmxTemplateResponseMixin, YearArchiveView):
    allow_empty = True
    date_field = "datetime"
    http_method_names = ["get"]
    make_object_list = True
    model = AuthenticatorLogItem
    ordering = "-datetime"
    paginate_by = 15
    partial_template_name = "terminusgps_authenticator/logs/partials/_year.html"
    template_name = "terminusgps_authenticator/logs/year.html"


class LogArchiveMonthView(HtmxTemplateResponseMixin, MonthArchiveView):
    allow_empty = True
    date_field = "datetime"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    month_format = "%m"
    ordering = "-datetime"
    paginate_by = 15
    partial_template_name = "terminusgps_authenticator/logs/partials/_month.html"
    template_name = "terminusgps_authenticator/logs/month.html"


class LogArchiveDayView(HtmxTemplateResponseMixin, DayArchiveView):
    allow_empty = True
    date_field = "datetime"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    month_format = "%m"
    ordering = "-datetime"
    paginate_by = 15
    partial_template_name = "terminusgps_authenticator/logs/partials/_day.html"
    template_name = "terminusgps_authenticator/logs/day.html"
