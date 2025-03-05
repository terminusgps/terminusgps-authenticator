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
    status = forms.NullBooleanField(
        required=False,
        widget=forms.widgets.Select(
            choices=[
                ("", "Punched in/out"),
                (True, "Punched in"),
                (False, "Punched out"),
            ],
            attrs={
                "class": "p-2 border-2 border-terminus-red-600 bg-gray-100 rounded w-full block"
            },
        ),
    )


class EmployeeBatchCreateForm(forms.Form):
    input_file = forms.FileField(
        label="Input file",
        allow_empty_file=False,
        validators=[validate_spreadsheet_file],
    )


class EmployeeCreateForm(forms.Form):
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
