from django.http import HttpRequest
from django.views.generic import TemplateView


class HtmxTemplateView(TemplateView):
    """
    Renders a partial HTML template depending on HTTP headers.

    `htmx documentation <https://htmx.org/docs/>`_

    """

    content_type = "text/html"
    partial_template_name: str | None = None
    """
    A partial template rendered by `htmx`_.

    .. _htmx: https://htmx.org/docs/

    :type: :py:obj:`str` | :py:obj:`None`
    :value: :py:obj:`None`
    """

    def setup(self, request: HttpRequest, *args, **kwargs) -> None:
        htmx_request = bool(request.headers.get("HX-Request"))
        boosted = bool(request.headers.get("HX-Boosted"))

        if htmx_request and self.partial_template_name and not boosted:
            self.template_name = self.partial_template_name
        return super().setup(request, *args, **kwargs)
