from .auth import LoginView, LogoutView
from .generic import (
    DashboardView,
    SettingsView,
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
    EmployeeSetFingerprintView,
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
    LogDetailView,
)
