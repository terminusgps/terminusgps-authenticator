from django.urls import path
from . import views

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),
    path("privacy/", views.PrivacyPolicyView.as_view(), name="privacy"),
    path("source/", views.SourceCodeView.as_view(), name="source"),
    path("employees/new/", views.EmployeeCreateView.as_view(), name="create employee"),
    path(
        "employees/new/batch/",
        views.EmployeeBatchCreateView.as_view(),
        name="create employee batch",
    ),
    path("employees/", views.EmployeeListView.as_view(), name="list employees"),
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
    path("logs/", views.LogArchiveIndexView.as_view(), name="logs index"),
    path(
        "logs/employees/<int:pk>/",
        views.EmployeeLogIndexView.as_view(),
        name="employee logs",
    ),
    path("logs/<int:year>/", views.LogArchiveYearView.as_view(), name="logs year"),
    path(
        "logs/<int:year>/<int:month>/",
        views.LogArchiveMonthView.as_view(),
        name="logs month",
    ),
    path(
        "logs/<int:year>/<int:month>/<int:day>/",
        views.LogArchiveDayView.as_view(),
        name="logs day",
    ),
    path("logs/<int:pk>/detail/", views.LogDetailView.as_view(), name="detail log"),
    path("reports/", views.ReportListView.as_view(), name="list reports"),
    path("reports/new/", views.ReportCreateView.as_view(), name="create report"),
    path("reports/<int:pk>/", views.ReportDetailView.as_view(), name="detail report"),
    path(
        "reports/<int:pk>/delete/",
        views.ReportDeleteView.as_view(),
        name="delete report",
    ),
]
