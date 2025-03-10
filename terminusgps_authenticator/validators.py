from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_spreadsheet_file(value: File) -> None:
    """Raises :py:exec:`~django.core.exceptions.ValidationError` if the file is not a spreadsheet file."""
    try:
        validator = FileExtensionValidator(allowed_extensions=["csv", "xlsx"])
        validator(value)
    except ValidationError:
        raise


def validate_email_unique(value: str) -> None:
    """Raises :py:exec:`~django.core.exceptions.ValidationError` if the email is non-unique among Django usernames."""
    filters = Q(username__iexact=value) | Q(email__iexact=value)
    queryset = get_user_model().objects.filter(filters)

    if queryset.exists():
        raise ValidationError(
            _("Whoops! '%(email)s' is taken."), code="invalid", params={"email": value}
        )
