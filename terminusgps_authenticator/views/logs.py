import calendar
from typing import Any

from django.views.generic import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    YearArchiveView,
)

from terminusgps_authenticator.models import AuthenticatorLogItem
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


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


class LogArchiveYearView(HtmxTemplateResponseMixin, YearArchiveView):
    allow_empty = True
    date_field = "datetime"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    ordering = "-datetime"
    paginate_by = 15
    partial_template_name = "terminusgps_authenticator/logs/partials/_year.html"
    template_name = "terminusgps_authenticator/logs/year.html"
    make_object_list = True

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["title"] = self.generate_title()
        return context

    def generate_title(self) -> str | None:
        """
        Generates a title for the view.

        :returns: A title, if it was generated.
        :rtype: :py:obj:`str` | :py:obj:`None`

        """
        return self.get_year()


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
