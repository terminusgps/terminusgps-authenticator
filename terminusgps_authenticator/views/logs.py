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
