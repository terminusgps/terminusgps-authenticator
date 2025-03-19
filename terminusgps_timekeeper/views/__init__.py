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
    EmployeeBatchCreateView,
    EmployeeListView,
    EmployeeSetFingerprintView,
)
from .reports import (
    ReportListView,
    ReportDetailView,
    ReportCreateView,
    ReportCreateSuccessView,
    ReportDownloadView,
)
from .shifts import ShiftListView
