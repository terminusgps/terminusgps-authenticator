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
from .reports import ReportListView
from .shifts import ShiftListView
