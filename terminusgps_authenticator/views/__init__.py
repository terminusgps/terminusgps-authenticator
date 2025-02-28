from .auth import LoginView, LogoutView
from .generic import LandingView, SettingsView
from .logs import LogItemListView, LogItemDetailView
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
