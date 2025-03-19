from typing import Any

from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from terminusgps_timekeeper.forms import ReportCreateForm
from terminusgps_timekeeper.models import Report
from terminusgps_timekeeper.pdf_generators import generate_report_pdf
from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin


class ReportListView(HtmxTemplateResponseMixin, ListView):
    content_type = "text/html"
    model = Report
    ordering = "end_date"
    paginate_by = 25
    partial_template_name = "terminusgps_timekeeper/reports/partials/_list.html"
    template_name = "terminusgps_timekeeper/reports/list.html"
    content_type = "text/html"
    extra_context = {
        "class": "flex flex-col gap-4",
        "title": "Reports",
        "latest": Report.objects.filter()[:5],
    }
    http_method_names = ["get"]


class ReportDetailView(HtmxTemplateResponseMixin, DetailView):
    content_type = "text/html"
    extra_context = {"class": "flex flex-col gap-4"}
    http_method_names = ["get"]
    model = Report
    partial_template_name = "terminusgps_timekeeper/reports/partials/_detail.html"
    template_name = "terminusgps_timekeeper/reports/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        report = self.get_object()
        context["title"] = f"Shifts between {report.start_date} and {report.end_date}"
        return context


class ReportCreateView(HtmxTemplateResponseMixin, CreateView):
    content_type = "text/html"
    extra_context = {
        "class": "flex flex-col gap-4 p-4 border rounded drop-shadow bg-white"
    }
    form_class = ReportCreateForm
    http_method_names = ["get", "post"]
    model = Report
    partial_template_name = "terminusgps_timekeeper/reports/partials/_create.html"
    template_name = "terminusgps_timekeeper/reports/create.html"
    success_url = reverse_lazy("create report success")

    def form_valid(self, form: ReportCreateForm) -> HttpResponse | HttpResponseRedirect:
        response = super().form_valid(form)
        generate_report_pdf(self.object, __class__.__name__)
        return response


class ReportCreateSuccessView(HtmxTemplateResponseMixin, TemplateView):
    content_type = "text/html"
    http_method_names = ["get"]
    partial_template_name = (
        "terminusgps_timekeeper/reports/partials/_create_success.html"
    )
    template_name = "terminusgps_timekeeper/reports/create_success.html"
    extra_context = {
        "class": "flex flex-col gap-4 p-4 border rounded drop-shadow bg-white"
    }


class ReportDownloadView(DetailView):
    content_type = "text/html"
    http_method_names = ["get"]
    model = Report
    template_name = "terminusgps_timekeeper/reports/download.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> FileResponse:
        return FileResponse(
            self.object.pdf.file.open(),
            as_attachment=True,
            filename=self.object.pdf.file.name,
        )
