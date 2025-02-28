from typing import Any
from django.views.generic import CreateView, DetailView, DeleteView
from django.http import HttpRequest, HttpResponseRedirect

from terminusgps_authenticator.models import AuthenticatorLogReport
from terminusgps_authenticator.views.base import HtmxTemplateView


class ReportCreateView(CreateView, HtmxTemplateView):
    template_name = "terminusgps_authenticator/reports/create.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_create.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]
    extra_context = {"class": ""}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = None
        return super().get_context_data(**kwargs)


class ReportDetailView(DetailView, HtmxTemplateView):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "delete"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponseRedirect:
        self.object = self.get_object()
        delete_view = ReportDeleteView()
        delete_view.request = request
        delete_view.args = args
        delete_view.kwargs = kwargs

        return delete_view.post(request, *args, **kwargs)


class ReportDeleteView(DeleteView, HtmxTemplateView):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["post"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)
