from typing import Sequence

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.mail import EmailMessage

from terminusgps_timekeeper.models import Report


if not hasattr(settings, "ADMINS"):
    raise ImproperlyConfigured("'ADMINS' setting is required.")


class ReportEmailerBase:
    def __init__(self, report: Report, to_addrs: Sequence[str], subject: str) -> None:
        self.report = report
        self.shifts = report.shifts.all()
        self.msg = EmailMessage(
            subject=subject,
            from_email="support@terminusgps.com",
            to=to_addrs,
            bcc=[admin[1] for admin in settings.ADMINS],
        )


class DailyReportEmailer(ReportEmailerBase):
    def __init__(
        self, report: Report, to_addrs: Sequence[str], subject="Daily Report"
    ) -> None:
        super().__init__(report, to_addrs, subject)


class WeeklyReportEmailer(ReportEmailerBase):
    def __init__(
        self, report: Report, to_addrs: Sequence[str], subject="Weekly Report"
    ) -> None:
        super().__init__(report, to_addrs, subject)


class MonthlyReportEmailer(ReportEmailerBase):
    def __init__(
        self, report: Report, to_addrs: Sequence[str], subject="Monthly Report"
    ) -> None:
        super().__init__(report, to_addrs, subject)


class YearlyReportEmailer(ReportEmailerBase):
    def __init__(
        self, report: Report, to_addrs: Sequence[str], subject="Yearly Report"
    ) -> None:
        super().__init__(report, to_addrs, subject)
