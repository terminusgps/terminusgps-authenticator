import datetime
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.rl_config import defaultPageSize

from django.utils import timezone

from terminusgps_authenticator.models import Report


styles = getSampleStyleSheet()
PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]


class ReportPdfGenerator:
    def __init__(self, report: Report) -> None:
        self.report = report
        self.doc = SimpleDocTemplate(self.generate_doc_name())
        self.story = [Spacer(1, 2 * inch)]
        self.style = styles["Normal"]
        for i in range(100):
            bogustext = ("This is Paragraph number %s. " % i) * 20
            p = Paragraph(bogustext, self.style)
            self.story.append(p)
            self.story.append(Spacer(1, 0.2 * inch))
        self.doc.build(
            self.story, onFirstPage=self.first_page, onLaterPages=self.later_page
        )

    @staticmethod
    def first_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Bold", 16)
        canvas.drawCenteredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 108, "Title String")
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(
            inch, 0.75 * inch, "First Page / %(info)s" % {"info": "pageinfo string"}
        )
        canvas.restoreState()

    @staticmethod
    def later_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Times-Roman", 9)
        canvas.drawString(
            inch, 0.75 * inch, "Page %d %s" % (doc.page, "pageinfo string")
        )
        canvas.restoreState()

    def generate_doc_name(self, timestamp: datetime.datetime | None = None) -> str:
        """
        Generates a name for the report pdf file based on a timestamp.

        :param timestamp: A timestamp.
        :type timestamp: :py:obj:`~datetime.datetime`
        :returns: A pdf filename.
        :rtype: :py:obj:`str`

        """
        return f"report_{timestamp or timezone.now():%Y%m%d_%H%M%S}.pdf"


def main() -> None:
    report = Report.objects.get(pk=2)
    ReportPdfGenerator(report)
    return


if __name__ == "__main__":
    main()
