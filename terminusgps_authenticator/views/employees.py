import pandas as pd
from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
    DeleteView,
)

from terminusgps_authenticator.models import AuthenticatorEmployee
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin
from terminusgps_authenticator.forms import (
    EmployeeBatchCreateForm,
    EmployeeCreateForm,
    EmployeeSearchForm,
)
from terminusgps_authenticator.utils import generate_random_password


class EmployeePunchInView(HtmxTemplateResponseMixin, TemplateView):
    template_name = "terminusgps_authenticator/employees/punch_in.html"
    partial_template_name = (
        "terminusgps_authenticator/employees/partials/_punch_in.html"
    )

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        super().setup(request, *args, **kwargs)
        try:
            self.object = AuthenticatorEmployee.objects.get(pk=self.kwargs["pk"])
        except AuthenticatorEmployee.DoesNotExist:
            self.object = None

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not self.object or self.object._punched_in:
            return HttpResponse(status=401)
        self.object._punched_in = False
        self.object.save()
        return super().get(request, *args, **kwargs)


class EmployeePunchOutView(HtmxTemplateResponseMixin, TemplateView):
    template_name = "terminusgps_authenticator/employees/punch_out.html"
    partial_template_name = (
        "terminusgps_authenticator/employees/partials/_punch_out.html"
    )


class EmployeeCreateView(HtmxTemplateResponseMixin, FormView):
    extra_context = {"class": "m-8 p-8 bg-gray-300 flex flex-col gap-4 rounded"}
    field_css_class = "p-2 rounded bg-white border border-gray-600"
    partial_template_name = "terminusgps_authenticator/employees/partials/_create.html"
    template_name = "terminusgps_authenticator/employees/create.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy("dashboard")
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeCreateForm) -> HttpResponseRedirect:
        username: str = form.cleaned_data["email"]
        password: str = generate_random_password()
        fingerprint_code: str = form.cleaned_data["code"]
        phone_number: str | None = form.cleaned_data["phone"]

        AuthenticatorEmployee.objects.create(
            user=get_user_model().objects.create_user(
                username=username, password=password
            ),
            code=fingerprint_code,
            phone=phone_number,
        )
        return HttpResponseRedirect(self.get_success_url())


class EmployeeListView(HtmxTemplateResponseMixin, ListView):
    http_method_names = ["get"]
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/list.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_list.html"
    ordering = "pk"
    paginate_by = 25
    extra_context = {"title": "Employees"}

    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        if self.request.GET.get("q"):
            queryset = queryset.filter(
                user__username__icontains=self.request.GET.get("q")
            )
        if self.request.GET.get("status"):
            queryset = queryset.filter(_punched_in=self.request.GET.get("status"))
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = EmployeeSearchForm(initial={"status": None})
        return context


class EmployeeBatchCreateView(HtmxTemplateResponseMixin, FormView):
    extra_context = {"class": "m-8 p-8 bg-gray-300 flex flex-col gap-4 rounded"}
    field_css_class = "p-2 rounded bg-white border border-gray-600"
    form_class = EmployeeBatchCreateForm
    partial_template_name = "terminusgps_authenticator/employees/_create_batch.html"
    success_url = reverse_lazy("list employees")
    template_name = "terminusgps_authenticator/employees/create_batch.html"
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeBatchCreateForm) -> HttpResponse:
        # Open the file as a dataframe and create a bunch of employees
        file = form.cleaned_data["input_file"]
        df: pd.DataFrame = pd.read_csv(file.file)
        print(f"{df.head() = }")
        return super().form_valid(form=form)

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["input_file"].widget.attrs.update({"class": self.field_css_class})
        return form


class EmployeeDetailView(HtmxTemplateResponseMixin, DetailView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/detail.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_detail.html"
    queryset = AuthenticatorEmployee.objects.all()
    context_object_name = "employee"
    http_method_names = ["get"]
    extra_context = {"class": "flex flex-col gap-8", "title": "Employee Details"}


class EmployeeUpdateView(HtmxTemplateResponseMixin, UpdateView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/update.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_update.html"
    queryset = AuthenticatorEmployee.objects.all()
    fields = ["user", "code"]
    context_object_name = "employee"
    http_method_names = ["get", "post"]


class EmployeeDeleteView(HtmxTemplateResponseMixin, DeleteView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/delete.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_delete.html"
    queryset = AuthenticatorEmployee.objects.all()
    context_object_name = "employee"
    http_method_names = ["get", "post"]
