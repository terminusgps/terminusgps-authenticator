from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from terminusgps_authenticator.views.base import HtmxTemplateView


class LandingView(HtmxTemplateView, LoginRequiredMixin):
    template_name = "terminusgps_authenticator/landing.html"
    partial_template_name = "terminusgps_authenticator/partials/_landing.html"
    login_url = reverse_lazy("login")
    raise_exception = False
    permission_denied_message = "Please login and try again."
    extra_context = {"class": "flex flex-col gap-8 bg-gray-300 rounded m-8 p-8"}


class SettingsView(HtmxTemplateView, LoginRequiredMixin):
    template_name = "terminusgps_authenticator/settings.html"
    partial_template_name = "terminusgps_authenticator/partials/_settings.html"
    login_url = reverse_lazy("login")
    raise_exception = False
    permission_denied_message = "Please login and try again."
