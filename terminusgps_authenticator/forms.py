from typing import Any
from django.core.exceptions import ValidationError
import pandas as pd
from django import forms
from django.utils.translation import gettext_lazy as _

from terminusgps_authenticator.models import AuthenticatorEmployee
from terminusgps_authenticator.validators import validate_csv_file


class EmployeeBatchCreateForm(forms.Form):
    input_file = forms.FileField(
        label="Input file", allow_empty_file=False, validators=[validate_csv_file]
    )

    def clean(self) -> None | dict[str, Any]:
        cleaned_data: None | dict[str, Any] = super().clean()
        if cleaned_data is not None:
            input_file = cleaned_data.get("input_file")

            if input_file is None:
                self.add_error(
                    "input_file",
                    ValidationError(
                        _("Whoops! No file provided."),
                        code="invalid",
                        params={"file": input_file},
                    ),
                )
                return cleaned_data

            input_df: pd.DataFrame = pd.read_csv(input_file)
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
