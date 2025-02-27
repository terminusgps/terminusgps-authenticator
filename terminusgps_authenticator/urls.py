from django.urls import path
from . import views

urlpatterns = [
    path("employees/new/", views.EmployeeCreateView.as_view(), name="create employee"),
    path(
        "employees/new/batch/",
        views.EmployeeBatchCreateView.as_view(),
        name="create employee batch",
    ),
    path("employees/list/", views.EmployeeListView.as_view(), name="list employees"),
    path(
        "employees/<int:pk>.<str:slug>/",
        views.EmployeeDetailView.as_view(),
        name="detail employee",
    ),
    path(
        "employees/<int:pk>.<str:slug>/update/",
        views.EmployeeUpdateView.as_view(),
        name="update employee",
    ),
    path(
        "employees/<int:pk>.<str:slug>/delete/",
        views.EmployeeDeleteView.as_view(),
        name="delete employee",
    ),
]
