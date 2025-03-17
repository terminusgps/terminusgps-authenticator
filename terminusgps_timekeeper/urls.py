from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
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
        "employees/<int:pk>/update/",
        views.EmployeeUpdateView.as_view(),
        name="update employee",
    ),
    path(
        "employees/<int:pk>/delete/",
        views.EmployeeDeleteView.as_view(),
        name="delete employee",
    ),
    path(
        "employees/<int:pk>/set-fingerprint/",
        views.EmployeeSetFingerprintView.as_view(),
        name="set fingerprint",
    ),
    path("reports/", views.ReportListView.as_view(), name="list reports"),
    path("shifts/<int:pk>/", views.ShiftListView.as_view(), name="list shifts"),
]
