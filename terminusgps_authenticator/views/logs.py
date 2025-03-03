import calendar

from typing import Any
from django.views.generic import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    YearArchiveView,
)

from terminusgps_authenticator.models import AuthenticatorLogItem
from terminusgps_authenticator.views.base import HtmxTemplateView


class LogArchiveIndexView(ArchiveIndexView, HtmxTemplateView):
    allow_empty = True
    date_field = "datetime"
    extra_context = {"title": "Logs"}
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    ordering = "-datetime"
    paginate_by = 10
    partial_template_name = "terminusgps_authenticator/logs/partials/_index.html"
    queryset = AuthenticatorLogItem.objects.filter()
    template_name = "terminusgps_authenticator/logs/index.html"
    context_object_name = "log_list"
    month_format = "%m"


class LogArchiveDayView(DayArchiveView, HtmxTemplateView):
    allow_empty = True
    model = AuthenticatorLogItem
    http_method_names = ["get"]
    queryset = AuthenticatorLogItem.objects.filter()
    template_name = "terminusgps_authenticator/logs/day.html"
    partial_template_name = "terminusgps_authenticator/logs/partials/_day.html"
    date_field = "datetime"
    month_format = "%m"
    paginate_by = 15
    ordering = "-datetime"

    def generate_title(self) -> str | None:
        """
        Generates a title for the view.

        If the month is invalid, i.e. not 1-12, this returns :py:obj:`None`.

        :returns: A title, if it was generated.
        :rtype: :py:obj:`str` | :py:obj:`None`

        """
        try:
            day, year = self.get_day(), self.get_year()
            month = calendar.month_name[self.get_month()]
            return f"{month} {day}, {year}"
        except IndexError:
            pass

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.generate_title()
        return context


class LogArchiveMonthView(MonthArchiveView, HtmxTemplateView):
    allow_empty = True
    model = AuthenticatorLogItem
    http_method_names = ["get"]
    queryset = AuthenticatorLogItem.objects.filter()
    template_name = "terminusgps_authenticator/logs/month.html"
    partial_template_name = "terminusgps_authenticator/logs/partials/_month.html"
    date_field = "datetime"
    month_format = "%m"
    paginate_by = 15
    ordering = "-datetime"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_dated_queryset()

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.generate_title()
        return context

    def generate_title(self) -> str | None:
        """
        Generates a title for the view.

        If the month is invalid, i.e. not 1-12, this returns :py:obj:`None`.

        :returns: A title, if it was generated.
        :rtype: :py:obj:`str` | :py:obj:`None`

        """
        try:
            year = self.get_year()
            month = calendar.month_name[self.get_month()]
            return f"{month} {year}"
        except IndexError:
            pass


class LogArchiveYearView(YearArchiveView, HtmxTemplateView):
    allow_empty = True
    model = AuthenticatorLogItem
    http_method_names = ["get"]
    template_name = "terminusgps_authenticator/logs/year.html"
    partial_template_name = "terminusgps_authenticator/logs/partials/_year.html"
    date_field = "datetime"
    paginate_by = 15
    ordering = "-datetime"

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.object_list = self.get_dated_queryset()
