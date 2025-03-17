from django.core.management.base import BaseCommand, CommandError
from terminusgps_authenticator.models import AuthenticatorEmployee


class Command(BaseCommand):
    help = "Adds a fingerprint code to an employee"

    def add_arguments(self, parser):
        """Adds arguments ``employee_id`` and ``fingerprint_code``."""
        parser.add_argument("employee_id", type=int)
        parser.add_argument("fingerprint_code", type=str)

    def handle(self, *args, **options):
        """
        Updates an employee's code to the provided fingerprint code.

        :param employee_id: An employee id.
        :type employee_id: :py:obj:`int`
        :param fingerprint_code: A new fingerprint code.
        :type fingerprint_code: :py:obj:`str`
        :raises CommandError: If ``employee_id`` was not provided.
        :raises CommandError: If ``fingerprint_code`` was not provided.
        :raises CommandError: If the employee wasn't found by id.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        employee_id: int | None = options.get("employee_id")
        fingerprint_code: str | None = options.get("fingerprint_code")

        if employee_id is None:
            raise CommandError(
                "Employee id was not provided, got '%(id)s'." % {"id": employee_id}
            )
        if fingerprint_code is None:
            raise CommandError(
                "Fingerprint code was not provided, got '%(code)s'."
                % {"code": fingerprint_code}
            )

        try:
            employee = AuthenticatorEmployee.objects.get(pk=employee_id)
            employee.code = fingerprint_code
            employee.save()
            self.stdout.write(
                self.style.SUCCESS(
                    "Successfully set employee #%(id)s's code to the provided fingerprint code."
                    % {"id": employee_id}
                )
            )
        except AuthenticatorEmployee.DoesNotExist:
            raise CommandError(
                "Employee #%(id)s was not found, it may not exist."
                % {"id": employee_id}
            )
