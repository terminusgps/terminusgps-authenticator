from typing import Any

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from django.views.generic import RedirectView, TemplateView

from terminusgps_authenticator.views.mixins import HtmxTemplateResponseMixin
from terminusgps_authenticator.models import AuthenticatorEmployee

if not hasattr(settings, "AUTHENTICATOR_REPO_URL"):
    raise ImproperlyConfigured("'AUTHENTICATOR_REPO_URL' setting is required.")


class DashboardView(LoginRequiredMixin, HtmxTemplateResponseMixin, TemplateView):
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    partial_template_name = "terminusgps_authenticator/partials/_dashboard.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "terminusgps_authenticator/dashboard.html"
    extra_context = {"title": "Dashboard"}

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context: dict[str, Any] = super().get_context_data(**kwargs)
        context["employee_data"] = {
            "Punched In": AuthenticatorEmployee.objects.filter(punched_in=True),
            "Punched Out": AuthenticatorEmployee.objects.filter(punched_in=False),
        }
        return context


class SettingsView(LoginRequiredMixin, HtmxTemplateResponseMixin, TemplateView):
    extra_context = {
        "class": "flex flex-col gap-8 bg-stone-100 rounded m-8 p-8",
        "title": "Settings",
    }
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    partial_template_name = "terminusgps_authenticator/partials/_settings.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "terminusgps_authenticator/settings.html"


class ContactView(HtmxTemplateResponseMixin, TemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_authenticator/partials/_contact.html"
    template_name = "terminusgps_authenticator/contact.html"
    extra_context = {"title": "Contact"}


class PrivacyPolicyView(HtmxTemplateResponseMixin, TemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_authenticator/partials/_privacy.html"
    template_name = "terminusgps_authenticator/privacy.html"
    extra_context = {"title": "Privacy Policy"}


class SourceCodeView(RedirectView):
    http_method_names = ["get"]
    permanent = True
    url = settings.AUTHENTICATOR_REPO_URL
