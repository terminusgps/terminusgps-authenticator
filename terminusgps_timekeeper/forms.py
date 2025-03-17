from uuid import uuid4

from django import forms
from django.core.validators import validate_email, validate_image_file_extension
from django.forms import widgets

from terminusgps_timekeeper.validators import (
    validate_spreadsheet_file,
    validate_email_unique,
)


class ReportFilterForm(forms.Form):
    paginate_by = forms.ChoiceField(
        required=False,
        initial=25,
        choices=((25, "25"), (50, "50"), (100, "100")),
        widget=widgets.Select(attrs={"class": "p-2 rounded border bg-white"}),
    )
    start_date = forms.DateField(
        required=False,
        widget=widgets.DateInput(
            attrs={"type": "date", "class": "p-2 rounded border bg-white"}
        ),
    )
    end_date = forms.DateField(
        required=False,
        widget=widgets.DateInput(
            attrs={"type": "date", "class": "p-2 rounded border bg-white"}
        ),
    )


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
