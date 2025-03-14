from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest
from django.views.generic import ListView

from terminusgps_authenticator.forms import ReportFilterForm
from terminusgps_authenticator.models import Report
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin


class ReportListView(HtmxTemplateResponseMixin, ListView):
    model = Report
    template_name = "terminusgps_authenticator/reports/list.html"
    partial_template_name = "terminusgps_authenticator/reports/partials/_list.html"
    paginate_by = 25

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        self.date_range = None
        form = ReportFilterForm(request.GET)
        if form.is_valid():
            self.paginate_by = form.cleaned_data["paginate_by"]
            self.start = form.cleaned_data["start_date"]
            self.end = form.cleaned_data["end_date"]
        super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        if self.start is not None:
            qs = qs.filter(start_datetime__lte=self.start)
        if self.end is not None:
            qs = qs.filter(end_datetime__gte=self.end)
        return qs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = ReportFilterForm(self.request.GET if self.request.GET else {})
        return context
