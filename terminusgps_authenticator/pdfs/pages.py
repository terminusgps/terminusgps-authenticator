from reportlab.platypus import PageTemplate

from terminusgps_authenticator.models import AuthenticatorLogReport


class ReportPageBase(PageTemplate):
    def __init__(self, report: AuthenticatorLogReport, id: str) -> None:
        self.report = report
        self.id = id


class ReportCoverPage(ReportPageBase):
    """Cover page for reports."""

    def __init__(
        self, report: AuthenticatorLogReport, id: str = "cover", *args, **kwargs
    ) -> None:
        super().__init__(report, id, *args, **kwargs)


class ReportLogsPage(ReportPageBase):
    """Logs page for reports."""

    def __init__(
        self, report: AuthenticatorLogReport, id: str = "logs", *args, **kwargs
    ) -> None:
        super().__init__(report, id, *args, **kwargs)


class ReportShiftsPage(ReportPageBase):
    """Shifts page for reports."""

    def __init__(
        self, report: AuthenticatorLogReport, id: str = "shifts", *args, **kwargs
    ) -> None:
        super().__init__(report, id, *args, **kwargs)
