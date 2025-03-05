from functools import wraps
from typing import Callable, Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from encrypted_model_fields.fields import EncryptedCharField


class LogAction(models.TextChoices):
    PUNCH_IN = "punch_in", _("Punched in")
    PUNCH_OUT = "punch_out", _("Punched out")
    ASSIGN_CODE = "assign_code", _("Assigned fingerprint code")


def create_logitem(action: str | None = None) -> Callable:
    """Creates a log item for the action name, if provided."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            result: Any = func(self, *args, **kwargs)
            if action and action.upper() in LogAction._member_names_:
                log_action = getattr(LogAction, action.upper())
                AuthenticatorLogItem.objects.create(
                    employee=self, action=log_action, datetime=timezone.now()
                )
            return result

        return wrapper

    return decorator


class AuthenticatorEmployee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT)
    """A Django user."""
    phone = models.CharField(max_length=12, blank=True, null=True, default=None)
    """An optional phone number."""
    code = EncryptedCharField(verbose_name="fingerprint code", max_length=2048)
    """A fingerprint code."""
    pfp = models.ImageField(
        verbose_name="profile picture", null=True, blank=True, default=None
    )
    """An optional profile picture image file."""
    title = models.CharField(max_length=64, null=True, blank=True, default=None)
    """An optional employee title."""
    _punched_in = models.BooleanField(default=False, db_column="punched_in")

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        """Returns the employee's username."""
        return str(self.user.username)

    def get_absolute_url(self) -> str:
        """Returns a URL pointing to the employee's detail view."""
        return reverse("detail employee", kwargs={"pk": self.pk})

    @property
    def email(self) -> str:
        """The employee's email, if it was set."""
        return self.user.email or self.user.username

    @property
    def punched_in(self) -> bool:
        """Whether or not the employee is currently punched in."""
        return bool(self._punched_in)

    @transaction.atomic
    @create_logitem(action="punch_in")
    def punch_in(self) -> None:
        """
        Punches the employee in.

        :raises AssertionError: If the employee was already punched in.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert not self._punched_in, "Employee is already punched in."
        self._punched_in = True

    @transaction.atomic
    @create_logitem(action="punch_out")
    def punch_out(self) -> None:
        """
        Punches the employee out.

        :raises AssertionError: If the employee was already punched out.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self._punched_in, "Employee is already punched out."
        self._punched_in = False

    @transaction.atomic
    @create_logitem(action="assign_code")
    def assign_code(self, fingerprint_code: str) -> None:
        """
        Assigns a fingerprint code to the employee.

        :param fingerprint_code: A fingerprint code.
        :type fingerprint_code: :py:obj:`str`
        :raises ValueError: If the fingerprint code is longer than 2048 characters.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if len(fingerprint_code) > 2048:
            raise ValueError(
                f"'fingerprint_code' cannot be longer than 2048 characters, got '{len(fingerprint_code)}'."
            )
        self.code = fingerprint_code


class AuthenticatorLogItem(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time for the log item."""
    employee = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorEmployee", on_delete=models.PROTECT
    )
    """Employee that created the log item."""
    action = models.CharField(
        max_length=1024, choices=LogAction.choices, default=LogAction.PUNCH_IN
    )
    """Action that was called to trigger logging."""

    class Meta:
        verbose_name = "log item"
        verbose_name_plural = "log items"

    def __str__(self) -> str:
        return str(self.employee)

    def get_absolute_url(self) -> str:
        return reverse("detail logitem", kwargs={"pk": self.pk})


class AuthenticatorLogReport(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time for the report."""
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    """User that triggered the report."""
    items = models.ManyToManyField("terminusgps_authenticator.AuthenticatorLogItem")
    """Log items selected for the report."""

    def __str__(self) -> str:
        return f"Report #{self.pk}"
