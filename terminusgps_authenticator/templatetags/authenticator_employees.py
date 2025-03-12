from typing import Any
from django.template import Library

from terminusgps_authenticator.models import AuthenticatorEmployee

register = Library()


@register.inclusion_tag("terminusgps_authenticator/employees/card.html")
def employee_card(
    employee: AuthenticatorEmployee,
    css_class: str | None = None,
    display_punch_state: bool = False,
) -> dict[str, Any]:
    return {
        "employee": employee,
        "id": f"employee-card-{employee.pk}",
        "display_punch_state": display_punch_state,
        "class": css_class
        or "w-full rounded border-2 border-terminus-red-600 bg-gray-100 p-4",
    }
