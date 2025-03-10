from datetime import datetime
from reportlab.pdfgen import canvas
from io import BytesIO
from django.db.models import QuerySet
from django.http import FileResponse, HttpRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, FormView, ListView
from django.utils import timezone

from terminusgps_authenticator.models import (
    AuthenticatorLogItem,
    AuthenticatorLogReport,
)
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

    def form_valid(self, form: ReportCreateForm) -> HttpResponseRedirect | HttpResponse:
        start, end = form.cleaned_data["start_date"], form.cleaned_data["end_date"]
        # TODO: Filter by employees
        # employees = form.cleaned_data["employees"]
        logs_qs = self.get_dated_logs(start, end)

        report = AuthenticatorLogReport.objects.create(
            datetime=timezone.now(), user=self.request.user
        )
        report.logs.set(logs_qs)
        report.save()
        return super().form_valid(form=form)

    def get_dated_logs(
        self, start: datetime, end: datetime
    ) -> QuerySet[AuthenticatorLogItem, AuthenticatorLogItem | None]:
        return AuthenticatorLogItem.objects.filter(
            datetime__gte=start, datetime__lte=end
        )


class ReportDetailView(DetailView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]


class ReportDownloadView(DetailView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/download.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_download.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]


class ReportDeleteView(DeleteView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/detail.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_detail.html"
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]
