from .auth import LoginView, LogoutView
from .generic import ContactView, PrivacyPolicyView, SourceCodeView
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
    ReportArchiveView,
    ReportDeleteView,
    report_download_view,
)
from .shifts import ShiftListView
