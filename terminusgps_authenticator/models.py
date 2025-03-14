from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

from encrypted_model_fields.fields import EncryptedCharField

from terminusgps_authenticator.utils import display_duration


class Employee(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self) -> str:
        """Returns the employee's username."""
        return str(self.user.username)

    def save(self, **kwargs) -> None:
        if self.pk:
            EmployeePunchCard.objects.get_or_create(employee=self)
        super().save(**kwargs)

    def get_absolute_url(self) -> str:
        """Returns a URL pointing to the employee's detail view."""
        return reverse("detail employee", kwargs={"pk": self.pk})

    @property
    def punched_in(self) -> bool:
        return self.punch_card.punched_in


class EmployeeShift(models.Model):
    employee = models.ForeignKey(
        "terminusgps_authenticator.Employee",
        on_delete=models.CASCADE,
        related_name="shifts",
    )
    """Employee that worked the shift."""
    start_datetime = models.DateTimeField()
    """Start date and time for the shift."""
    end_datetime = models.DateTimeField()
    """End date and time for the shift."""
    duration = models.DurationField(blank=True, null=True, default=None)
    """Duration of the shift."""

    class Meta:
        verbose_name = "shift"
        verbose_name_plural = "shifts"

    def __str__(self) -> str:
        return f"{self.employee} shift #{self.pk}"

    def save(self, **kwargs) -> None:
        if not self.duration:
            self.duration = self.end_datetime - self.start_datetime
        super().save(**kwargs)

    def get_duration_display(self) -> str:
        return display_duration(self.duration.total_seconds())


class EmployeePunchCard(models.Model):
    employee = models.OneToOneField(
        "terminusgps_authenticator.Employee",
        on_delete=models.CASCADE,
        related_name="punch_card",
    )
    """An employee."""
    punched_in = models.BooleanField(default=False)
    """Whether or not the employee is currently punched in."""
    last_punch_in_time = models.DateTimeField(null=True, blank=True, default=None)
    """Last date and time the employee punched in."""
    _prev_punch_state = models.BooleanField(default=False)
    """Previous punch in state for the employee."""

    class Meta:
        verbose_name = "punch card"
        verbose_name_plural = "punch cards"

    def __str__(self) -> str:
        return f"{self.employee.user.username}'s Punch Card"

    def save(self, **kwargs) -> None:
        if self.pk and self._prev_punch_state != self.punched_in:
            if self._prev_punch_state is True and self.punched_in is False:
                EmployeeShift.objects.create(
                    employee=self.employee,
                    start_datetime=self.last_punch_in_time,
                    end_datetime=timezone.now(),
                )
            else:
                self.last_punch_in_time = timezone.now()
            self._prev_punch_state = self.punched_in
        super().save(**kwargs)


class Report(models.Model):
    start_date = models.DateField()
    """Start of the report date range."""
    end_date = models.DateField()
    """End of the report date range."""
    pdf = models.FileField(null=True, blank=True, default=None)
    """A programatically generated pdf file of the report."""

    class Meta:
        verbose_name = "report"
        verbose_name_plural = "reports"

    def __str__(self) -> str:
        return f"Report #{self.pk}"

    def save(self, **kwargs) -> None:
        if self.pk and not self.pdf:
            # TODO: Create a pdf of the report for emails
            self.pdf = None
        super().save(**kwargs)

    @property
    def shifts(self) -> models.QuerySet[EmployeeShift | EmployeeShift]:
        return EmployeeShift.objects.filter(
            start_datetime__gte=self.start_date, end_datetime__lte=self.end_date
        )
