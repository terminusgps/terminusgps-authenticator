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
from .shifts import (
    ShiftArchiveIndexView,
    ShiftYearArchiveView,
    ShiftMonthArchiveView,
    ShiftDayArchiveView,
    ShiftWeekArchiveView,
)
