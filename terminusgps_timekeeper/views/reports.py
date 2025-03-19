from typing import Any

from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ArchiveIndexView,
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
)

from terminusgps_timekeeper.forms import ReportCreateForm
from terminusgps_timekeeper.models import Report
from terminusgps_timekeeper.pdf_generators import generate_report_pdf
from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin


class ReportArchiveView(HtmxTemplateResponseMixin, ArchiveIndexView):
    content_type = "text/html"
    date_field = "end_date"
    extra_context = {"title": "All Reports", "class": "flex flex-col gap-4"}
    http_method_names = ["get"]
    model = Report
    ordering = "end_date"
    paginate_by = 25
    partial_template_name = "terminusgps_timekeeper/reports/partials/_archive.html"
    template_name = "terminusgps_timekeeper/reports/archive.html"


class ReportListView(HtmxTemplateResponseMixin, ListView):
    content_type = "text/html"
    content_type = "text/html"
    extra_context = {"class": "flex flex-col gap-4", "title": "Reports"}
    http_method_names = ["get"]
    model = Report
    ordering = "end_date"
    paginate_by = 25
    partial_template_name = "terminusgps_timekeeper/reports/partials/_list.html"
    template_name = "terminusgps_timekeeper/reports/list.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["latest"] = Report.objects.filter()[:5]
        return context


class ReportDetailView(HtmxTemplateResponseMixin, DetailView):
    content_type = "text/html"
    extra_context = {"class": "flex flex-col gap-4", "title": "Report Details"}
    http_method_names = ["get"]
    model = Report
    partial_template_name = "terminusgps_timekeeper/reports/partials/_detail.html"
    template_name = "terminusgps_timekeeper/reports/detail.html"


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

    def get_success_url(self) -> str:
        if self.object is not None:
            return f"{reverse('create report success')}?next={reverse('download report', kwargs={'pk': self.object.pk})}"
        return super().get_success_url()


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

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        self.next = request.GET.get("next")
        print(f"{self.next = }")


class ReportDownloadView(DetailView):
    content_type = "text/html"
    http_method_names = ["get"]
    model = Report
    template_name = "terminusgps_timekeeper/reports/download.html"

    def get(self, request: HttpRequest, *args, **kwargs) -> FileResponse:
        pdf_file = generate_report_pdf(self.get_object())
        return FileResponse(pdf_file, as_attachment=True, filename="report.pdf")


def report_download_view(
    request: HttpRequest, *args, **kwargs
) -> FileResponse | HttpResponse:
    try:
        report = Report.objects.get(pk=kwargs["pk"])
    except Report.DoesNotExist:
        return HttpResponse(status=404)

    pdf_file = generate_report_pdf(report)
    return FileResponse(pdf_file, as_attachment=True, filename="report.pdf")


class ReportDeleteView(DeleteView):
    content_type = "text/html"
    model = Report
    http_method_names = ["post"]
    template_name = "terminusgps_timekeeper/reports/delete.html"
    success_url = reverse_lazy("archive reports")
