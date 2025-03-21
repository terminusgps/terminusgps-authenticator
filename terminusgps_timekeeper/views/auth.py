from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as LoginViewBase
from django.contrib.auth.views import LogoutView as LogoutViewBase
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from terminusgps_timekeeper.views.mixins import HtmxTemplateResponseMixin


class LoginView(HtmxTemplateResponseMixin, LoginViewBase):
    template_name = "terminusgps_timekeeper/login.html"
    partial_template_name = "terminusgps_timekeeper/partials/_login.html"
    success_url = reverse_lazy("dashboard")
    extra_context = {"title": "Login", "class": "flex flex-col gap-4 p-4"}

    def get_success_url(self) -> str:
        return str(self.success_url)

    def form_valid(self, form: AuthenticationForm) -> HttpResponseRedirect:
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_form(self, form_class=None) -> AuthenticationForm:
        css_class = "p-2 bg-white border rounded"

        username_attrs = {
            "class": css_class,
            "placeholder": "email@terminusgps.com",
            "autofocus": True,
        }
        password_attrs = {"class": css_class}

        form = super().get_form(form_class)
        form.fields["username"].widget.attrs.update(username_attrs)
        form.fields["password"].widget.attrs.update(password_attrs)
        return form


class LogoutView(HtmxTemplateResponseMixin, LogoutViewBase):
    http_method_names = ["get", "post"]
    template_name = "terminusgps_timekeeper/logout.html"
    partial_template_name = "terminusgps_timekeeper/partials/_logout.html"
    extra_context = {
        "class": "group m-4 flex cursor-pointer select-none items-center gap-2 rounded border border-gray-600 bg-gray-300 p-2 drop-shadow-sm hover:border-terminus-red-300 transition-colors duration-300 ease-in-out"
    }

    def get_success_url(self) -> str:
        return reverse("login")
