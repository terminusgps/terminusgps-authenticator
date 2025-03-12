from typing import Any
from uuid import uuid4

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, validate_image_file_extension
from django.forms import widgets
from django.utils.translation import gettext_lazy as _

from terminusgps_authenticator.models import AuthenticatorEmployee
from terminusgps_authenticator.validators import (
    validate_spreadsheet_file,
    validate_email_unique,
)


class SettingsForm(forms.Form): ...


class ReportCreateForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.widgets.DateInput(
            attrs={"type": "date", "class": "p-2 bg-white rounded border"}
        )
    )
    end_date = forms.DateField(
        widget=forms.widgets.DateInput(
            attrs={"type": "date", "class": "p-2 bg-white rounded border"}
        )
    )
    employees = forms.ModelMultipleChoiceField(
        queryset=AuthenticatorEmployee.objects.all(),
        widget=forms.widgets.CheckboxSelectMultiple(
            attrs={"class": "p-2 bg-white rounded border"}
        ),
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
                "autofocus": True,
                "autocomplete": "off",
            }
        ),
    )
    status = forms.ChoiceField(
        choices=[("", "Punched in/out"), ("in", "Punched in"), ("out", "Punched out")],
        required=False,
        widget=forms.widgets.RadioSelect(
            attrs={
                "class": "p-2 border-2 border-terminus-red-600 bg-gray-100 rounded w-full block"
            }
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
        validators=[validate_image_file_extension],
        widget=widgets.FileInput(
            attrs={"class": "p-2 rounded bg-white border border-gray-600"}
        ),
    )
    email = forms.EmailField(
        label="Employee Email",
        validators=[validate_email, validate_email_unique],
        widget=widgets.EmailInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": "email@terminusgps.com",
            }
        ),
    )
    title = forms.CharField(
        label="Employee Title",
        required=False,
        widget=widgets.TextInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": "L1 Engineer",
            }
        ),
    )
    phone = forms.CharField(
        label="Employee Phone #",
        required=False,
        widget=widgets.TextInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": "+15555555555",
            }
        ),
    )
    code = forms.CharField(
        label="Fingerprint Code",
        required=False,
        widget=widgets.TextInput(
            attrs={
                "class": "p-2 rounded bg-white border border-gray-600",
                "placeholder": str(uuid4()),
            }
        ),
    )
