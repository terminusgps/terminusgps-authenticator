from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet
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
    _prev_punch_state = models.BooleanField(default=False)
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


class AuthenticatorEmployeeShift(models.Model):
    start_datetime = models.DateTimeField()
    """Start date and time for the shift."""
    end_datetime = models.DateTimeField()
    """End date and time for the shift."""
    employee = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorEmployee", on_delete=models.CASCADE
    )
    """Employee that worked the shift."""
    duration = models.DurationField(blank=True, null=True, default=None)
    """Duration of the shift."""
    report = models.ForeignKey(
        "terminusgps_authenticator.AuthenticatorLogReport",
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    """Report that generated the shift."""

    class Meta:
        verbose_name = "shift"
        verbose_name_plural = "shifts"

    def __str__(self) -> str:
        return f"{self.employee} shift #{self.pk}"

    def save(self, **kwargs) -> None:
        if not self.duration:
            self.duration = self.end_datetime - self.start_datetime
        super().save(**kwargs)


class AuthenticatorLogReport(models.Model):
    datetime = models.DateTimeField(default=timezone.now)
    """Date and time the report was created."""
    user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)
    """User that created the report."""
    pdf = models.FileField(null=True, blank=True, default=None)
    """A programatically generated pdf file for the report."""
    logs = models.ManyToManyField("terminusgps_authenticator.AuthenticatorLogItem")
    """Logs selected for the report."""

    class Meta:
        verbose_name = "report"
        verbose_name_plural = "reports"

    def __str__(self) -> str:
        return f"Report #{self.pk}"

    def get_absolute_url(self) -> str:
        """Returns a URL pointing to the report's detail view."""
        return reverse("detail report", kwargs={"pk": self.pk})

    def get_unique_employee_ids(self) -> list[int]:
        """Retrieves a list of employee ids for the report."""
        assert self.logs.exists(), "Report logs were not set."
        unique_ids: list[int] = []
        seen_ids: set[int] = set()

        for log in self.logs.all():
            if log.employee.pk not in seen_ids:
                unique_ids.append(log.employee.pk)
                seen_ids.add(log.employee.pk)
        return unique_ids

    def generate_employee_shifts(
        self, employee_id: int
    ) -> list[AuthenticatorEmployeeShift | None]:
        """Generates and returns a list of shifts for the employee by id."""
        assert self.logs.exists(), "Report logs were not set."
        punch_in, punch_out = LogAction.PUNCH_IN, LogAction.PUNCH_OUT
        actions: list[LogAction] = [punch_in, punch_out]
        shifts: list[AuthenticatorEmployeeShift | None] = []
        queryset: QuerySet = self.logs.filter(employee__pk=employee_id)
        prev: AuthenticatorLogItem | None = None

        for curr in queryset.order_by("datetime"):
            if curr.action not in actions:
                continue

            if prev and prev.action == punch_in and curr.action == punch_out:
                shifts.append(
                    AuthenticatorEmployeeShift.objects.create(
                        start_datetime=prev.datetime,
                        end_datetime=curr.datetime,
                        employee=curr.employee,
                        report=self,
                    )
                )
                prev: AuthenticatorLogItem | None = None
            else:
                prev: AuthenticatorLogItem | None = (
                    curr if curr.action == punch_in else None
                )

        return shifts
