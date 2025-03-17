from typing import Any
from django.views.generic.base import TemplateResponseMixin


class HtmxTemplateResponseMixin(TemplateResponseMixin):
    """
    Renders a partial HTML template depending on HTTP headers.

    `htmx documentation <https://htmx.org/docs/>`_

    """

    partial_template_name: str | None = None
    """
    A partial template rendered by `htmx`_.

    .. _htmx: https://htmx.org/docs/

    :type: :py:obj:`str` | :py:obj:`None`
    :value: :py:obj:`None`
    """

    def render_to_response(self, context: dict[str, Any], **response_kwargs):
        htmx_request = self.request.headers.get("HX-Request", False)
        boosted = self.request.headers.get("HX-Boosted", False)

        if htmx_request and self.partial_template_name and not boosted:
            self.template_name = self.partial_template_name
        return super().render_to_response(context, **response_kwargs)
