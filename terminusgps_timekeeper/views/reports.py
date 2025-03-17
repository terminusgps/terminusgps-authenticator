from typing import Any

from django.db.models import QuerySet
from django.views.generic import DetailView, ListView

from terminusgps_timekeeper.forms import ReportFilterForm
from terminusgps_timekeeper.models import Report
from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin


class ReportListView(HtmxTemplateResponseMixin, ListView):
    model = Report
    ordering = "end_date"
    paginate_by = 25
    partial_template_name = "terminusgps_timekeeper/reports/partials/_list.html"
    template_name = "terminusgps_timekeeper/reports/list.html"
    content_type = "text/html"
    extra_context = {"class": "flex flex-col gap-4", "title": "Reports"}

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        form = ReportFilterForm(self.request.GET if self.request.GET else {})
        if form.is_valid():
            start, end = form.cleaned_data["start_date"], form.cleaned_data["end_date"]
            if start is not None:
                qs = qs.filter(start_datetime__lte=start)
            if end is not None:
                qs = qs.filter(end_datetime__gte=end)
        return qs

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = ReportFilterForm(self.request.GET if self.request.GET else {})
        return context


class ReportDetailView(HtmxTemplateResponseMixin, DetailView):
    model = Report
    template_name = "terminusgps_timekeeper/reports/detail.html"
    partial_template_name = "terminusgps_timekeeper/reports/partials/_detail.html"
    extra_context = {"class": "flex flex-col gap-4"}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        report = self.get_object()
        context["title"] = f"Shifts between {report.start_date} and {report.end_date}"
        return context
