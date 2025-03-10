from django.contrib.auth.base_user import AbstractBaseUser
import pandas as pd
from typing import Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files import File
from django.db.models import Q, QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, FormView, ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from terminusgps_authenticator.models import AuthenticatorEmployee, AuthenticatorLogItem
from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin
from terminusgps_authenticator.forms import (
    EmployeeBatchCreateForm,
    EmployeeCreateForm,
    EmployeeSearchForm,
)
from terminusgps_authenticator.utils import generate_random_password


class EmployeeCreateView(HtmxTemplateResponseMixin, FormView):
    extra_context = {"class": "flex flex-col gap-4", "title": "Create Employee"}
    field_css_class = "p-2 rounded bg-white border border-gray-600"
    partial_template_name = "terminusgps_authenticator/employees/partials/_create.html"
    template_name = "terminusgps_authenticator/employees/create.html"
    form_class = EmployeeCreateForm
    success_url = reverse_lazy("list employees")
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeCreateForm) -> HttpResponseRedirect:
        username: str = form.cleaned_data["email"]
        password: str = generate_random_password()
        fingerprint_code: str | None = form.cleaned_data["code"]
        phone_number: str | None = form.cleaned_data["phone"]
        profile_picture: File | None = form.cleaned_data["pfp"]

        AuthenticatorEmployee.objects.create(
            user=get_user_model().objects.create_user(
                username=username, password=password
            ),
            code=fingerprint_code,
            phone=phone_number,
            pfp=profile_picture,
        )
        return HttpResponseRedirect(self.get_success_url())


class EmployeeListView(HtmxTemplateResponseMixin, ListView):
    http_method_names = ["get"]
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/list.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_list.html"
    ordering = "user__username"
    paginate_by = 5
    extra_context = {"title": "Employees"}

    def get_queryset(self, **kwargs) -> QuerySet:
        queryset = super().get_queryset(**kwargs)
        q, status = self.request.GET.get("q"), self.request.GET.get("status")
        form = EmployeeSearchForm({"q": q, "status": status})
        if q and form.is_valid():
            filters = Q(user__username__iexact=q) | Q(user__username__istartswith=q)
            queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["form"] = EmployeeSearchForm()
        return context


class EmployeeBatchCreateView(HtmxTemplateResponseMixin, FormView):
    extra_context = {"class": "flex flex-col gap-4", "title": "Upload Batch File"}
    form_class = EmployeeBatchCreateForm
    partial_template_name = "terminusgps_authenticator/employees/_create_batch.html"
    success_url = reverse_lazy("list employees")
    template_name = "terminusgps_authenticator/employees/create_batch.html"
    http_method_names = ["get", "post"]

    def form_valid(self, form: EmployeeBatchCreateForm) -> HttpResponse:
        try:
            df = self.get_dataframe(form.cleaned_data["input_file"])
        except ValueError as e:
            form.add_error(
                "input_file",
                ValidationError(
                    _("Whoops! %(error)s"), code="invalid", params={"error": e}
                ),
            )
            return self.form_invalid(form=form)

        if df is None:
            form.add_error(
                "input_file",
                ValidationError(
                    _(
                        "Whoops! Failed to extract data from the input file. Please try again later."
                    )
                ),
            )
            return self.form_invalid(form=form)

        for i, row in df.iterrows():
            email: str = str(row["Email"])
            phone: str | None = str(row["Phone"]) if pd.notna(row["Phone"]) else None
            title: str | None = str(row["Title"]) if pd.notna(row["Title"]) else None
            user: AbstractBaseUser = get_user_model().objects.create_user(
                username=email, password=generate_random_password()
            )
            AuthenticatorEmployee.objects.create(user=user, phone=phone, title=title)
        return super().form_valid(form=form)

    def get_dataframe(self, input_file: File) -> pd.DataFrame | None:
        ext = "".join(input_file.name.split(".")[-1])

        match ext:
            case "csv":
                df = pd.read_csv(input_file)
            case "xlsx":
                df = pd.read_excel(input_file)
            case _:
                raise ValueError(f"Invalid input file type: '{ext}'.")
        return self.validate_dataframe(df)

    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """Raises :py:exec:`~django.core.exceptions.ValidationError` if any invalid columns are present in the :py:obj:`~pandas.DataFrame`."""
        target_cols: tuple[str, str, str] = ("Email", "Phone", "Title")
        bad_cols: list[str] = [col for col in df.columns if col not in target_cols]

        if bad_cols:
            raise ValueError(f"Invalid column names: '{bad_cols}'")
        return df


class EmployeeDetailView(SuccessMessageMixin, HtmxTemplateResponseMixin, DetailView):
    model = AuthenticatorEmployee
    template_name = "terminusgps_authenticator/employees/detail.html"
    partial_template_name = "terminusgps_authenticator/employees/partials/_detail.html"
    queryset = AuthenticatorEmployee.objects.all()
    context_object_name = "employee"
    http_method_names = ["get", "patch"]
    extra_context = {"class": "flex flex-col gap-8", "title": "Employee Details"}
    success_message = "'%(name)s' was %(action)s successfully."

    def patch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.headers.get("HX-Request"):
            return HttpResponse(status=403)
        status = request.GET.get("status")

        if status is not None:
            employee = self.get_object()
            employee.punched_in = True if status == "true" else False
            employee.save()
        return self.get(request, *args, **kwargs)

    def get_success_message(self, cleaned_data: dict[str, Any]) -> str:
        latest_log = self.object.get_latest_log()
        return self.success_message % dict(
            cleaned_data,
            name=self.object.user.username,
            action=latest_log.get_action_display(),
        )


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
