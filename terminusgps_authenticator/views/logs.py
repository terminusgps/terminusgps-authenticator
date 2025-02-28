from typing import Any
from django.views.generic import ListView, DetailView

from terminusgps_authenticator.models import AuthenticatorLogItem
from terminusgps_authenticator.views.base import HtmxTemplateView


class LogItemListView(ListView, HtmxTemplateView):
    context_object_name = "logitem"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    paginate_by = 25
    partial_template_name = "terminusgps_authenticator/logs/partials/_list.html"
    queryset = AuthenticatorLogItem.objects.all()
    template_name = "terminusgps_authenticator/logs/list.html"
    ordering = "-datetime"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object_list = self.get_queryset().order_by(self.get_ordering())
        return super().get_context_data(**kwargs)


class LogItemDetailView(DetailView, HtmxTemplateView):
    context_object_name = "logitem"
    http_method_names = ["get"]
    model = AuthenticatorLogItem
    partial_template_name = "terminusgps_authenticator/logs/partials/_detail.html"
    queryset = AuthenticatorLogItem.objects.all()
    template_name = "terminusgps_authenticator/logs/detail.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        self.object = self.get_object()
        return super().get_context_data(**kwargs)
