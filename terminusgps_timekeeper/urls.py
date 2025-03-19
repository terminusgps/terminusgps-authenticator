from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("privacy/", views.PrivacyPolicyView.as_view(), name="privacy"),
    path("source/", views.SourceCodeView.as_view(), name="source"),
    path("employees/", views.EmployeeListView.as_view(), name="list employees"),
    path("employees/new/", views.EmployeeCreateView.as_view(), name="create employee"),
    path(
        "employees/new/batch/",
        views.EmployeeBatchCreateView.as_view(),
        name="create employee batch",
    ),
    path(
        "employees/<int:pk>/",
        views.EmployeeDetailView.as_view(),
        name="detail employee",
    ),
    path(
        "employees/<int:pk>/set-fingerprint/",
        views.EmployeeSetFingerprintView.as_view(),
        name="set fingerprint",
    ),
    path("reports/", views.ReportListView.as_view(), name="list reports"),
    path("reports/new/", views.ReportCreateView.as_view(), name="create report"),
    path(
        "reports/success/",
        views.ReportCreateSuccessView.as_view(),
        name="create report success",
    ),
    path("reports/archive/", views.ReportArchiveView.as_view(), name="archive reports"),
    path(
        "reports/<int:pk>/download/", views.report_download_view, name="download report"
    ),
    path(
        "reports/<int:pk>/delete/",
        views.ReportDeleteView.as_view(),
        name="delete report",
    ),
    path("reports/<int:pk>/", views.ReportDetailView.as_view(), name="detail report"),
    path("shifts/<int:pk>/", views.ShiftListView.as_view(), name="list shifts"),
]
