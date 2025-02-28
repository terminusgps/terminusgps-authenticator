from django.core.files import File
from django.core.validators import FileExtensionValidator


def validate_spreadsheet_file(value: File) -> None:
    """Raises :py:exec:`~django.core.exceptions.ValidationError` if the file is not a spreadsheet file."""
    validator = FileExtensionValidator(allowed_extensions=["csv", "xlsx"])
    validator(value)
