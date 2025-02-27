from django.contrib.auth import get_user_model
import pandas as pd
import pathlib

from typing import Any

from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    FormView,
    ListView,
    UpdateView,
    DeleteView,
)

from terminusgps_authenticator.models import AuthenticatorEmployee
from terminusgps_authenticator.views.base import HtmxTemplateView
from terminusgps_authenticator.forms import EmployeeBatchCreateForm, EmployeeCreateForm


class EmployeeCreateView(FormView, HtmxTemplateView):
    extra_context = {"class": "m-8 p-8 bg-gray-300 flex flex-col gap-4 rounded"}
    field_css_class = "p-2 rounded bg-white border border-gray-600"
    partial_template_name = "terminusgps_authenticator/employees/partials/_create.html"
    template_name = "terminusgps_authenticator/employees/create.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy("landing")
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeCreateForm) -> HttpResponseRedirect:
        print(f"{get_user_model().objects.__dir__() = }")
        username = form.cleaned_data["email"]
        phone_number = form.cleaned_data["phone"]
        password = "Terminus#1!"
        fingerprint_code = form.cleaned_data["code"]

        AuthenticatorEmployee.objects.create(
            user=get_user_model().objects.create_user(
                username=username,
                password=password,
            ),
            code=fingerprint_code,
            phone=phone_number,
        )
        return HttpResponseRedirect(self.get_success_url())


class EmployeeListView(ListView, HtmxTemplateView):
    http_method_names = ["get"]
    model = AuthenticatorEmployee
    queryset = AuthenticatorEmployee.objects.all()
    template_name = "terminusgps_authenticator/employees/list.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_list.html"
    ordering = "pk"
    paginate_by = 25

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = self.get_queryset().order_by(self.get_ordering())
        return super().get_context_data(**kwargs)


class EmployeeBatchCreateView(FormView, HtmxTemplateView):
    extra_context = {"class": "m-8 p-8 bg-gray-300 flex flex-col gap-4 rounded"}
    field_css_class = "p-2 rounded bg-white border border-gray-600"
    form_class = EmployeeBatchCreateForm
    partial_template_name = "terminusgps_authenticator/employees/_create_batch.html"
    success_url = reverse_lazy("list employees")
    template_name = "terminusgps_authenticator/employees/create_batch.html"
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeBatchCreateForm) -> HttpResponse:
        # Open the file as a dataframe and create a bunch of employees
        filepath: pathlib.Path = pathlib.Path(form.cleaned_data["input_file"].file)
        df = pd.read_csv(filepath)
        for _ in range(len(df)):
            # Create employee on every row
            print(f"{df.iloc[0] = }")
            print(f"{df.iloc[1][1] = }")
            print(f"{df.iloc[0][1] = }")
        return super().form_valid(form=form)

    def get_form(self, form_class=None) -> forms.Form:
        form = super().get_form(form_class)
        form.fields["input_file"].widget.attrs.update({"class": self.field_css_class})
        return form


class EmployeeDetailView(DetailView, HtmxTemplateView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/detail.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_detail.html"
    queryset = AuthenticatorEmployee.objects.all()
    fields = ["user", "code"]
    context_object_name = "employee"
    http_method_names = ["get"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)


class EmployeeUpdateView(UpdateView, HtmxTemplateView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/update.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_update.html"
    queryset = AuthenticatorEmployee.objects.all()
    fields = ["user", "code"]
    context_object_name = "employee"
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)


class EmployeeDeleteView(DeleteView, HtmxTemplateView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/delete.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_delete.html"
    queryset = AuthenticatorEmployee.objects.all()
    context_object_name = "employee"
    http_method_names = ["get", "post"]

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)
