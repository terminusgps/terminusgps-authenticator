from typing import Any
from uuid import uuid4

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from terminusgps_authenticator.models import AuthenticatorEmployee
from terminusgps_authenticator.validators import validate_spreadsheet_file


class ReportCreateForm(forms.Form):
    start_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.widgets.DateInput(attrs={"type": "date"}))
    employees = forms.ModelMultipleChoiceField(
        queryset=AuthenticatorEmployee.objects.all()
    )

    def clean(self) -> dict[str, Any] | None:
        cleaned_data: dict[str, Any] | None = super().clean()
        if cleaned_data:
            start_date = cleaned_data.get("start_date")
            end_date = cleaned_data.get("end_date")
            date_diff = end_date - start_date

            if date_diff.days < 0:
                raise ValidationError(
                    _("Whoops! Invalid start/end date combination."), code="invalid"
                )

        return cleaned_data


class EmployeeSearchForm(forms.Form):
    q = forms.CharField(
        required=False,
        widget=forms.widgets.TextInput(
            attrs={
                "class": "p-2 border-2 border-terminus-red-600 bg-gray-100 rounded w-full block",
                "placeholder": "Search...",
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        widget=forms.widgets.RadioSelect(
            choices=[
                ("", "Punched in/out"),
                ("in", "Punched in"),
                ("out", "Punched out"),
            ]
        ),
    )


class EmployeeBatchCreateForm(forms.Form):
    input_file = forms.FileField(
        label="Input file",
        allow_empty_file=False,
        validators=[validate_spreadsheet_file],
        widget=widgets.FileInput(
            attrs={"class": "p-2 rounded bg-white border border-gray-600"}
        ),
    )


class EmployeeCreateForm(forms.Form):
    pfp = forms.FileField(
        allow_empty_file=True,
        required=False,
        label="Employee Profile Picture",
        widget=widgets.FileInput(
            attrs={"class": "p-2 rounded bg-white border border-gray-600"}
        ),
    )
    email = forms.EmailField(
        label="Employee Email",
        validators=[validate_email],
        widget=widgets.EmailInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": "email@terminusgps.com",
            }
        ),
    )
    phone = forms.CharField(
        label="Employee Phone #",
        widget=widgets.TextInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": "+15555555555",
            }
        ),
    )
    code = forms.CharField(
        label="Fingerprint Code",
        widget=widgets.TextInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": str(uuid4()),
            }
        ),
    )

    def clean(self) -> None | dict[str, Any]:
        cleaned_data: None | dict[str, Any] = super().clean()
        if cleaned_data is not None:
            username = cleaned_data.get("email")
            all_usernames = [user.username for user in get_user_model().objects.all()]

            if username in all_usernames:
                self.add_error(
                    "email",
                    ValidationError(
                        _("Whoops! '%(email)s' is already taken."),
                        code="invalid",
                        params={"email": username},
                    ),
                )
        return cleaned_data


class FingerprintAuthenticationForm(forms.Form):
    id = forms.HiddenInput()
    code = forms.CharField(max_length=256)

    def clean(self) -> None | dict[str, Any]:
        cleaned_data: None | dict[str, Any] = super().clean()
        if cleaned_data:
            emp_id = cleaned_data.get("id")
            emp_code = cleaned_data.get("code")

            if emp_id and emp_code:
                try:
                    employee = AuthenticatorEmployee.objects.get(pk=int(emp_id))
                except AuthenticatorEmployee.DoesNotExist:
                    self.add_error(
                        "id",
                        forms.ValidationError(
                            _("Whoops! Employee with id '%(id)s' was not found."),
                            code="invalid",
                            params={"id": id},
                        ),
                    )
                else:
                    if employee.code != emp_code:
                        self.add_error(
                            "code",
                            forms.ValidationError(
                                _(
                                    "Whoops! The fingerprint did not match employee #%(id)s."
                                ),
                                code="invalid",
                                params={"id": id},
                            ),
                        )
        return cleaned_data
