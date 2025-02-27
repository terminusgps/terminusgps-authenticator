from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("employees/new/", views.EmployeeCreateView.as_view(), name="create employee"),
    path(
        "employees/new/batch/",
        views.EmployeeBatchCreateView.as_view(),
        name="create employee batch",
    ),
    path("employees/list/", views.EmployeeListView.as_view(), name="list employees"),
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
]
