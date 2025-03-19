from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import RedirectView, TemplateView

from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin

if not hasattr(settings, "TIMEKEEPER_REPO_URL"):
    raise ImproperlyConfigured("'TIMEKEEPER_REPO_URL' setting is required.")


class ContactView(HtmxTemplateResponseMixin, TemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_timekeeper/partials/_contact.html"
    template_name = "terminusgps_timekeeper/contact.html"
    extra_context = {"title": "Contact"}


class PrivacyPolicyView(HtmxTemplateResponseMixin, TemplateView):
    http_method_names = ["get"]
    partial_template_name = "terminusgps_timekeeper/partials/_privacy.html"
    template_name = "terminusgps_timekeeper/privacy.html"
    extra_context = {
        "title": "Privacy Policy",
        "class": "p-2 border rounded bg-white drop-shadow-sm",
    }


class SourceCodeView(RedirectView):
    http_method_names = ["get"]
    permanent = True
    url = settings.TIMEKEEPER_REPO_URL
