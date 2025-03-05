from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, FormView, ListView

from terminusgps_authenticator.models import AuthenticatorLogReport
from terminusgps_authenticator.forms import ReportCreateForm
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


class ReportCreateView(FormView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/create.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_create.html"
    http_method_names = ["get", "post"]
    form_class = ReportCreateForm
    extra_context = {"title": "New Report"}
    success_url = reverse_lazy("list reports")


class ReportDetailView(DetailView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]


class ReportDeleteView(DeleteView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]
