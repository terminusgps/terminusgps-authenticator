from typing import Any
from django.views.generic import CreateView, DetailView, DeleteView, ListView

from terminusgps_authenticator.models import AuthenticatorLogReport
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


class ReportListView(ListView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/list.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_list.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]
    queryset = AuthenticatorLogReport.objects.all()
    ordering = "-datetime"
    paginate_by = 25
    extra_context = {"title": "Reports"}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = self.get_queryset().order_by(self.get_ordering())
        return super().get_context_data(**kwargs)


class ReportCreateView(CreateView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/create.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_create.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]
    extra_context = {"class": ""}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = None
        return super().get_context_data(**kwargs)


class ReportDetailView(DetailView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)


class ReportDeleteView(DeleteView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)
