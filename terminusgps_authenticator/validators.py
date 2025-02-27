from django.core.files import File
from django.core.validators import FileExtensionValidator


def validate_csv_file(value: File) -> None:
    """Raises :py:exec:`~django.core.exceptions.ValidationError` if the file is not a csv file."""
    validator = FileExtensionValidator(allowed_extensions=["csv"])
    validator(value)
