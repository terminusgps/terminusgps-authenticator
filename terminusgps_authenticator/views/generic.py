from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from terminusgps_authenticator.views.base import HtmxTemplateView


class LandingView(LoginRequiredMixin, HtmxTemplateView):
    extra_context = {"class": "flex flex-col gap-8 bg-stone-100 rounded m-8 p-8"}
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    partial_template_name = "terminusgps_authenticator/partials/_landing.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "terminusgps_authenticator/landing.html"


class SettingsView(LoginRequiredMixin, HtmxTemplateView):
    extra_context = {"class": "flex flex-col gap-8 bg-stone-100 rounded m-8 p-8"}
    http_method_names = ["get"]
    login_url = reverse_lazy("login")
    partial_template_name = "terminusgps_authenticator/partials/_settings.html"
    permission_denied_message = "Please login and try again."
    raise_exception = False
    template_name = "terminusgps_authenticator/settings.html"
