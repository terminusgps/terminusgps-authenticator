import io
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

from django.conf import settings
from django.db.models import Sum
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Image,
    Spacer,
    TableStyle,
    Table,
)

from terminusgps_timekeeper.models import Employee, Report
from terminusgps_timekeeper.utils import display_duration


class PDFReportGenerator:
    def __init__(self, report: Report) -> None:
        self.report = report
        self.filename = f"report_{report.pk}_{report.start_date}_{report.end_date}.pdf"
        self.buffer = io.BytesIO()
        self.doc = SimpleDocTemplate(
            self.buffer,
            pagesize=letter,
            rightMargin=0.5 * inch,
            leftMargin=0.5 * inch,
            topMargin=0.5 * inch,
            bottomMargin=0.5 * inch,
        )
        self.styles = getSampleStyleSheet()
        self.elements = []

        self.styles.add(
            ParagraphStyle(
                name="Title", parent=self.styles["Heading1"], fontsize=24, alignment=1
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="Subtitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                alignment=1,
            )
        )
        self.styles.add(
            ParagraphStyle(
                name="TableHeader",
                parent=self.styles["Normal"],
                fontSize=12,
                alignment=1,
                fontname="Helvetica-Bold",
            )
        )

    def _add_cover_page(self) -> None:
        logo_path = os.path.join(
            settings.BASE_DIR
            / "terminusgps_timekeeper"
            / "static"
            / "terminusgps_timekeeper"
            / "logo.svg"
        )

        if os.path.exists(logo_path):
            logo = Image(logo_path, width=2 * inch, height=2 * inch)
            logo.hAlign = "CENTER"
            self.elements.append(logo)

        self.elements.append(Spacer(1, 1 * inch))

        if self.report.end_date - self.report.start_date <= datetime.timedelta(days=1):
            report_type = "Daily Report"
        elif self.report.end_date - self.report.start_date <= datetime.timedelta(
            days=7
        ):
            report_type = "Weekly Report"
        elif self.report.end_date - self.report.start_date <= datetime.timedelta(
            weeks=4
        ):
            report_type = "Monthly Report"
        else:
            report_type = "Yearly Report"

        self.elements.append(Paragraph("Terminus GPS Timekeeper", self.styles["Title"]))
        self.elements.append(Spacer(1, 0.25 * inch))
        self.elements.append(Paragraph(report_type, self.styles["Subtitle"]))
        self.elements.append(Spacer(1, 0.25 * inch))
        self.elements.append(
            Paragraph(
                f"Report period: {self.report.start_date} to {self.report.end_date}",
                self.styles["Subtile"],
            )
        )
        self.elements.append(Spacer(1, 2 * inch))
        self.elements.append(
            Paragraph(f"Generated on: {timezone.now()}", self.styles["Normal"])
        )
        self.elements.append(PageBreak())

    def _add_overview_page(self) -> None:
        self.elements.append(Paragraph("Employee Hours", self.styles["Heading1"]))
        self.elements.append(Spacer(1, 0.5 * inch))

        if not self.report.shifts.exists():
            self.elements.append(
                Paragraph("No shifts recorded for this preiod.", self.styles["Normal"])
            )
            self.elements.append(PageBreak())
            return

        employee_hours = {}
        for employee in Employee.objects.filter(
            shifts__in=self.report.shifts
        ).distinct():
            total_duration = self.report.shifts.filter(employee=employee).aggregate(
                total=Sum("duration")
            )["total"] or datetime.timedelta(0)
            employee_hours[str(employee)] = total_duration.total_seconds() / 3600

        plt.figure(sigsize=(8, 4))
        employees = list(employee_hours.keys())
        hours = list(employee_hours.values())

        employees, hours = zip(
            *sorted(zip(employees, hours), key=lambda x: x[1], reverse=True)
        )
        y_pos = np.arange(len(employees))
        plt.barh(y_pos, hours, align="center")
        plt.yticks(y_pos, employees)
        plt.xlabel("Hours")
        plt.title("Total hours by employee")

        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        plt.close()

        chart_image = Image(img_buffer, width=7 * inch, height=4 * inch)
        self.elements.append(chart_image)
        self.elements.append(Spacer(1, 0.5 * inch))
        self.elements.append(Paragraph("Hours Summary", self.styles["Heading2"]))
        self.elements.append(Spacer(1, 0.25 * inch))

        data = [["Employee", "Hours", "Duration"]]
        for name, hours in zip(employees, hours):
            duration_str = display_duration(hours * 3600)
            data.append([name, f"{hours:.2f}", duration_str])

        total_hours = sum(hours)
        total_duration = display_duration(total_hours * 3600)
        data.append(["Total", f"{total_hours:.2f}", total_duration])
        table = Table(data)
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("ALIGN", (0, 0), (-1, 0), "CENTER"),
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, 0), colors.black),
                ]
            )
        )
        self.elements.append(table)
        self.elements.append(PageBreak())
