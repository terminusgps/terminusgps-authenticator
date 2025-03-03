from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from django.conf import settings, ImproperlyConfigured

from terminusgps_authenticator.views.base import HtmxTemplateView

if not hasattr(settings, "AUTHENTICATOR_REPO_URL"):
    raise ImproperlyConfigured("'AUTHENTICATOR_REPO_URL' setting is required.")


class DashboardView(LoginRequiredMixin, HtmxTemplateView):
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    partial_template_name = "terminusgps_authenticator/partials/_dashboard.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "terminusgps_authenticator/dashboard.html"
    extra_context = {"title": "Dashboard"}


class SettingsView(LoginRequiredMixin, HtmxTemplateView):
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


class AboutView(HtmxTemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_authenticator/partials/_about.html"
    template_name = "terminusgps_authenticator/about.html"
    extra_context = {"title": "About"}


class ContactView(HtmxTemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_authenticator/partials/_contact.html"
    template_name = "terminusgps_authenticator/contact.html"
    extra_context = {"title": "Contact"}


class PrivacyPolicyView(HtmxTemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_authenticator/partials/_privacy.html"
    template_name = "terminusgps_authenticator/privacy.html"
    extra_context = {"title": "Privacy Policy"}


class SourceCodeView(RedirectView):
    http_method_names = ["get"]
    permanent = True
    url = settings.AUTHENTICATOR_REPO_URL
