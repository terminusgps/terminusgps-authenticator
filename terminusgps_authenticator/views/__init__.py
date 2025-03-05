from .auth import LoginView, LogoutView
from .generic import (
    DashboardView,
    SettingsView,
    AboutView,
    ContactView,
    PrivacyPolicyView,
    SourceCodeView,
)
from .employees import (
    EmployeeCreateView,
    EmployeeDetailView,
    EmployeeUpdateView,
    EmployeeDeleteView,
    EmployeeBatchCreateView,
    EmployeeListView,
)
from .reports import (
    ReportCreateView,
    ReportDetailView,
    ReportDeleteView,
    ReportListView,
)
from .logs import (
    LogArchiveIndexView,
    LogArchiveYearView,
    LogArchiveMonthView,
    LogArchiveDayView,
    EmployeeLogIndexView,
)
