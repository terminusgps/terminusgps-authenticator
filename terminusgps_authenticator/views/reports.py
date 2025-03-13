from typing import Any
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, DeleteView, FormView, ListView

from terminusgps_authenticator.forms import ReportCreateForm
from terminusgps_authenticator.models import (
    AuthenticatorLogItem,
    AuthenticatorLogReport,
)
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


class ReportListView(LoginRequiredMixin, ListView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/list.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_list.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]
    queryset = AuthenticatorLogReport.objects.all()
    ordering = "-datetime"
    paginate_by = 25
    extra_context = {"title": "Reports"}
    login_url = reverse_lazy("login")
    permission_denied_message = "Please login and try again."
    raise_exception = False


class ReportCreateView(FormView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/create.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_create.html"
    http_method_names = ["get", "post"]
    form_class = ReportCreateForm
    extra_context = {"title": "New Report", "class": "flex flex-col gap-4"}
    success_url = reverse_lazy("list reports")

    def form_valid(self, form: ReportCreateForm) -> HttpResponseRedirect | HttpResponse:
        start, end = form.cleaned_data["start_date"], form.cleaned_data["end_date"]
        employees = form.cleaned_data["employees"]
        logs_qs = self.get_dated_logs(start, end)

        if employees is not None:
            logs_qs = logs_qs.filter(employee__in=employees)

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
    http_method_names = ["get", "patch"]
    context_object_name = "report"
    extra_context = {"title": "Report Details"}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        start_date, end_date = self.get_object().date_range
        context["start_date"] = start_date
        context["end_date"] = end_date
        return context


class ReportDownloadView(DetailView, HtmxTemplateResponseMixin):
    template_name = "terminusgps_authenticator/reports/download.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_download.html"
    model = AuthenticatorLogReport
    http_method_names = ["get"]
    context_object_name = "report"


class ReportDeleteView(DeleteView):
    model = AuthenticatorLogReport
    http_method_names = ["get", "post"]
