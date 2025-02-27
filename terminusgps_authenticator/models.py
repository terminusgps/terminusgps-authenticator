from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class AuthenticatorPunchState(models.TextChoices):
    IN = "in", _("Punch in")
    OUT = "out", _("Punch out")


class AuthenticatorEmployee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.PROTECT)
    """Django user for the employee."""
    phone = models.CharField(max_length=12, blank=True, null=True, default=None)
    """An optional phone number for the employee."""
    code = models.CharField(verbose_name="fingerprint code", max_length=2048)
    """A fingerprint code for the employee."""
    slug = models.SlugField(blank=True, null=True, default=None)
    """A slug generated from the employee's name."""
    pstate = models.CharField(
        verbose_name="punch state",
        max_length=3,
        choices=AuthenticatorPunchState.choices,
        default=AuthenticatorPunchState.IN,
    )
    """The current punch state of the employee."""

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        """Returns the employee's username."""
        return str(self.user.username)

    @property
    def email(self) -> str:
        """The employee's email, if it was set."""
        return self.user.email if self.user.email else self.user.username

    @transaction.atomic
    def assign_code(self, fingerprint_code: str) -> None:
        """
        Assigns a fingerprint code to the employee.

        TODO: Clean/validate the code.

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

    def get_absolute_url(self) -> str:
        return reverse("detail employee", kwargs={"pk": self.pk})


class AuthenticatorLogItem(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time for the log item."""
    employee = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorEmployee", on_delete=models.PROTECT
    )
    """Employee that created the log item."""
    pstate = models.CharField(
        verbose_name="punch state",
        max_length=3,
        choices=AuthenticatorPunchState.choices,
    )
    """Punch state of the employee at the time of logging."""

    class Meta:
        verbose_name = "log item"
        verbose_name_plural = "log items"

    def __str__(self) -> str:
        return str(self.employee)
