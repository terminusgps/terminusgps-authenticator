from typing import Any
from django.template import Library

register = Library()


@register.inclusion_tag("terminusgps_authenticator/charts/bars.html")
def bars_chart(name: str, data: dict[str, str | int | float]) -> dict[str, Any]:
    if not all([val.isdigit() for val in data.values() if isinstance(val, str)]):
        raise ValueError("All values must be digits.")

    return {"id": name.lower(), "name": name, "class": "", "data": data}


@register.inclusion_tag("terminusgps_authenticator/charts/dots.html")
def dots_chart(name: str, data: dict[str, str | int | float]) -> dict[str, Any]:
    if not all([val.isdigit() for val in data.values() if isinstance(val, str)]):
        raise ValueError("All values must be digits.")

    return {"id": name.lower(), "name": name, "class": "", "data": data}


@register.inclusion_tag("terminusgps_authenticator/charts/hash.html")
def hash_chart(name: str, data: dict[str, str | int | float]) -> dict[str, Any]:
    if not all([val.isdigit() for val in data.values() if isinstance(val, str)]):
        raise ValueError("All values must be digits.")

    return {"id": name.lower(), "name": name, "class": "", "data": data}


@register.inclusion_tag("terminusgps_authenticator/charts/pie.html")
def pie_chart(name: str, data: dict[str, str | int | float]) -> dict[str, Any]:
    if not all([val.isdigit() for val in data.values() if isinstance(val, str)]):
        raise ValueError("All values must be digits.")

    return {"id": name.lower(), "name": name, "class": "", "data": data}
