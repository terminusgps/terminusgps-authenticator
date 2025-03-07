from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from encrypted_model_fields.fields import EncryptedCharField


class LogAction(models.TextChoices):
    PUNCH_IN = "punch_in", _("Punched in")
    PUNCH_OUT = "punch_out", _("Punched out")
    ASSIGN_CODE = "assign_code", _("Assigned fingerprint code")
    CREATED = "created", _("Created")
    UNKNOWN = "unknown", _("Unknown action")


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
    punched_in = models.BooleanField(default=False)
    """Whether or not the employee is currently punched in."""
    _prev_punch_state = models.BooleanField(null=True, blank=True, default=None)
    _prev_fingerprint_code = EncryptedCharField(
        null=True, blank=True, default=None, max_length=2048
    )

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        """Returns the employee's username."""
        return str(self.user.username)

    def save(self, **kwargs) -> None:
        """Checks if the employee's attributes were updated and generates a log if necessary."""
        if self.pk:
            now = timezone.now()
            action = LogAction.UNKNOWN

            if self.punched_in != self._prev_punch_state:
                punched_in = self._prev_punch_state is False and self.punched_in is True
                action = LogAction.PUNCH_IN if punched_in else LogAction.PUNCH_OUT

                AuthenticatorLogItem.objects.create(
                    employee=self, datetime=now, action=action
                )
                self._prev_punch_state = self.punched_in

            if self.code != self._prev_fingerprint_code:
                self._prev_fingerprint_code = self.code
                action = LogAction.ASSIGN_CODE

                AuthenticatorLogItem.objects.create(
                    employee=self, datetime=now, action=action
                )

        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """Returns a URL pointing to the employee's detail view."""
        return reverse("detail employee", kwargs={"pk": self.pk})

    def get_latest_log(self):
        qs = AuthenticatorLogItem.objects.filter(employee=self).order_by("-datetime")

        if qs.exists():
            return qs.first()


class AuthenticatorLogItem(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time for the log item."""
    employee = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorEmployee", on_delete=models.PROTECT
    )
    """Employee that created the log item."""
    action = models.CharField(
        max_length=1024, choices=LogAction.choices, default=LogAction.UNKNOWN
    )
    """Action that was called to trigger logging."""

    class Meta:
        verbose_name = "log"
        verbose_name_plural = "logs"

    def __str__(self) -> str:
        return f"{str(self.employee)} - #{self.pk}"

    def get_absolute_url(self) -> str:
        return reverse("detail logitem", kwargs={"pk": self.pk})


class AuthenticatorLogReport(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time the report was created."""
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    """User that created the report."""
    logs = models.ManyToManyField("terminusgps_authenticator.AuthenticatorLogItem")
    """Logs selected for the report."""
    file = models.FileField(null=True, blank=True, default=None)
    """A programatically generated pdf file for the report."""

    class Meta:
        verbose_name = "report"
        verbose_name_plural = "reports"

    def __str__(self) -> str:
        return f"Report #{self.pk}"


class AuthenticatorEmployeeShift(models.Model):
    start_datetime = models.DateTimeField()
    """Start date and time for the shift."""
    end_datetime = models.DateTimeField()
    """End date and time for the shift."""
    employee = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorEmployee", on_delete=models.CASCADE
    )
    """Employee that worked the shift."""
    tdelta = models.DurationField(blank=True, null=True, default=None)
    """Time difference between start and end datetimes."""

    class Meta:
        verbose_name = "shift"
        verbose_name_plural = "shifts"

    def __str__(self) -> str:
        return f"Shift #{self.pk}"

    def save(self, **kwargs) -> None:
        if not self.tdelta:
            self.tdelta = self.end_datetime - self.start_datetime
        super().save(**kwargs)
