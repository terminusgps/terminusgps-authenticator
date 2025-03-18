import datetime
import io
import os
import pathlib

import matplotlib.pyplot as plt
import numpy as np

from django.db.models import Sum
from django.utils import timezone

from reportlab import platypus
from reportlab.lib import colors
from reportlab.lib import pagesizes
from reportlab.lib import styles
from reportlab.lib import units
from terminusgps_timekeeper.models import Employee, Report
from terminusgps_timekeeper.utils import display_duration


def generate_report_pdf(report: Report) -> Report:
    """
    Generates a pdf file for the provided report and saves it.

    :param report: A report.
    :type report: :py:obj:`~terminusgps_timekeeper.models.Report`
    :returns: The report, with a pdf file generated and saved for it.
    :rtype: :py:obj:`~terminusgps_timekeeper.models.Report`

    """
    return PDFReportGenerator(report).generate()


class PDFReportGenerator:
    """A generator class for report pdf files."""

    def __init__(self, report: Report) -> None:
        """
        Generates basic styles, sets :py:attr:`elements` to any empty list, sets :py:attr:`report` to the provided report and generates a filename for the pdf file.

        :param report: A report.
        :type report: :py:obj:`~terminusgps_timekeeper.models.Report`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.elements = []
        self.report: Report = report
        self.styles: styles.StyleSheet1 = styles.getSampleStyleSheet()
        self.filename: str = (
            f"report_{report.pk}_{report.start_date}_{report.end_date}.pdf"
        )

        self.buffer = io.BytesIO()
        self.doc = self._create_doc(self.buffer)
        self.styles.add(
            styles.ParagraphStyle(
                name="DocTitle",
                parent=self.styles["Heading1"],
                fontsize=24,
                alignment=1,
            )
        )
        self.styles.add(
            styles.ParagraphStyle(
                name="DocSubtitle",
                parent=self.styles["Heading2"],
                fontSize=16,
                alignment=1,
            )
        )
        self.styles.add(
            styles.ParagraphStyle(
                name="TableHeader",
                parent=self.styles["Normal"],
                fontSize=12,
                alignment=1,
                fontname="Helvetica-Bold",
            )
        )

    @property
    def report_period(self) -> str:
        """Shortcut property for :py:meth:`get_report_period`"""
        return self.get_report_period()

    @property
    def report_type(self) -> str:
        """Shortcut property for :py:meth:`get_report_type`"""
        return self.get_report_type()

    def get_report_period(self) -> str:
        """
        Returns a subtitle based on the report's period.

        :returns: A report period.
        :rtype: :py:obj:`str`

        """
        return f"Report period: {self.report.start_date} to {self.report.end_date}"

    def get_report_type(self) -> str:
        """
        Returns a report type string based on the report time period.

        :returns: A report type.
        :rtype: :py:obj:`str`

        """
        match (self.report.end_date - self.report.start_date).days:
            case 0 | 1:
                return "Daily Report"
            case 2 | 3 | 4 | 5 | 6 | 7:
                return "Weekly Report"
            case d if 8 <= d <= 31:
                return "Monthly Report"
            case _:
                return "Yearly Report"

    def get_employee_hours(self) -> dict:
        """
        Returns a dictionary containing all employees and their aggregate hours in the report period.

        :returns: A dictionary of employees and work hours.
        :rtype: :py:obj:`dict`

        """
        return {
            str(employee): (
                self.report.shifts.filter(employee=employee).aggregate(
                    total=Sum("duration")
                )["total"]
                or datetime.timedelta(0)
            ).total_seconds()
            / 3600
            for employee in Employee.objects.filter(
                shifts__in=self.report.shifts
            ).distinct()
        }

    def add_spacer(
        self, width: float = 1, height: float = 0.25, unit: float = units.inch
    ) -> None:
        """
        Adds a spacer to the document.

        :param width: Width of the spacer.
        :type width: :py:obj:`float`
        :param height: Height of the spacer.
        :type height: :py:obj:`float`
        :param unit: A measurement unit. Default is :py:obj:`~reportlab.lib.units.inch`.
        :type unit: :py:obj:`float`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.elements.append(platypus.Spacer(width, height * unit))

    def add_paragraph(self, text: str, style: styles.PropertySet) -> None:
        """
        Adds a paragraph to the document.

        :param text: Text for the paragraph.
        :type text: :py:obj:`str`
        :param style: Style for the paragraph.
        :type style: :py:obj:`~reportlab.lib.styles.PropertySet`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.elements.append(platypus.Paragraph(text, style))

    def add_pagebreak(self) -> None:
        """
        Adds a pagebreak to the document.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.elements.append(platypus.PageBreak())

    def add_image_file(
        self,
        filepath: pathlib.Path,
        width: float,
        height: float,
        halign: str | None = "CENTER",
    ) -> None:
        """
        Adds an image file to the document.

        :param path: An image filepath.
        :type path: :py:obj:`~pathlib.Path`
        :param width: Width for the image.
        :type width: :py:obj:`float`
        :param height: Height for the image.
        :type height: :py:obj:`float`
        :param halign: Horizontal alignment of the image within the document. Default is ``"CENTER"``.
        :type halign: :py:obj:`str`
        :raises ValueError: If the image file does not exist.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not filepath or not os.path.exists(filepath):
            raise ValueError(f"'{filepath}' was not found.")

        image: platypus.Image = platypus.Image(filepath, width=width, height=height)
        self._add_image(image, halign)

    def add_image_buffer(
        self, buffer: io.BytesIO, width: float, height: float, halign: str | None = None
    ) -> None:
        """
        Adds an image buffer to the document.

        :param buffer: A binary data stream.
        :type buffer: :py:obj:`~io.BytesIO`
        :param width: Width for the image.
        :type width: :py:obj:`float`
        :param height: Height for the image.
        :type height: :py:obj:`float`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        image: platypus.Image = platypus.Image(buffer, width=width, height=height)
        self._add_image(image, halign)

    def add_table(self, data: list[list[str]]) -> None:
        """
        Adds a table to the document.

        :param data: Data to be rendered in a table.
        :type data: :py:obj:`list`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        available_width: float = self.doc.width
        colwidths: list[float] = [available_width / len(data[0])] * len(data[0])
        table: platypus.Table = platypus.Table(data, colWidths=colwidths)

        table.setStyle(
            platypus.TableStyle(
                [
                    ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                    ("ALIGN", (2, 0), (2, -1), "RIGHT"),
                    ("GRID", (0, 0), (-1, 0), 1, colors.black),
                    ("BOX", (0, 0), (-1, -1), 1, colors.black),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                    ("WIDTH", (0, 0), (-1, -1), available_width),
                ]
            )
        )
        self.elements.append(table)

    def generate(self) -> Report:
        """
        Generates a PDF file based on :py:attr:`report` and saves it.

        :returns: The report.
        :rtype: :py:obj:`~terminusgps_timekeeper.models.Report`

        """
        self._add_cover_page()
        self._add_overview_page()
        self._add_employee_shift_tables()

        self.doc.build(self.elements)
        self.buffer.seek(0)
        self.report.pdf.save(self.filename, self.buffer, save=True)
        return self.report

    @staticmethod
    def _create_doc(buffer: io.BytesIO) -> platypus.SimpleDocTemplate:
        """
        Creates a :py:obj:`~reportlab.platypus.SimpleDocTemplate` for the report.

        :param buffer: A binary data stream.
        :type buffer: :py:obj:`~io.BytesIO`
        :returns: A simple doc template for the report pdf file.
        :rtype: :py:obj:`~reportlab.platypus.SimpleDocTemplate`

        """
        return platypus.SimpleDocTemplate(
            buffer,
            pagesize=pagesizes.letter,
            rightMargin=0.5 * units.inch,
            leftMargin=0.5 * units.inch,
            topMargin=0.5 * units.inch,
            bottomMargin=0.5 * units.inch,
        )

    def _add_image(self, image: platypus.Image, halign: str | None) -> None:
        """
        Adds an image to the document.

        :param image: An image.
        :type image: :py:obj:`~reportlab.platypus.Image`
        :param halign: Horizontal alignment for the image.
        :type halign: :py:obj:`str` | :py:obj:`None`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if halign is not None:
            image.hAlign = halign
        self.elements.append(image)

    def _add_cover_page(self) -> None:
        """
        Adds a cover page to the document.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.add_paragraph("Terminus GPS Timekeeper", self.styles["DocTitle"])
        self.add_spacer(1, 0.25)
        self.add_paragraph(self.report_type, self.styles["DocSubtitle"])
        self.add_spacer(1, 0.25)
        self.add_paragraph(self.report_period, self.styles["DocSubtitle"])
        self.add_spacer(1, 6)
        self.add_paragraph(
            f"Generated on: {timezone.now():%Y-%m-%d %H:%M:%S:%f}",
            self.styles["Normal"],
        )
        self.add_pagebreak()

    def _add_overview_page(self) -> None:
        """
        Adds an overview page to the document.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.add_paragraph("Employee Hours", self.styles["Heading1"])
        self.add_spacer(1, 0.5)
        if not self.report.shifts.exists():
            self.add_paragraph(
                "No shifts recorded for this period.", self.styles["Normal"]
            )
            self.add_pagebreak()
            return

        employee_hours = self.get_employee_hours()
        plt.figure(figsize=(8, 4))
        employees = list(employee_hours.keys())
        hours = list(employee_hours.values())
        sorted_data = sorted(zip(employees, hours), key=lambda x: x[1], reverse=True)
        employees = [item[0] for item in sorted_data]
        hours_list = [item[1] for item in sorted_data]
        y_pos = np.arange(len(employees))
        plt.barh(y_pos, hours_list, align="center")
        plt.yticks(y_pos, employees)
        plt.xlabel("Hours")
        plt.title("Total hours by employee")
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        plt.close()

        self.add_image_buffer(img_buffer, width=7 * units.inch, height=4 * units.inch)
        self.add_spacer(1, 0.5)
        self.add_paragraph("Hours Summary", self.styles["Heading2"])
        self.add_spacer(1, 0.25)

        data = [["Employee", "Hours", "Duration"]]
        for name, hours_value in zip(employees, hours_list):
            duration_str = display_duration(hours_value * 3600)
            data.append([name, f"{hours_value:.2f}", duration_str])

        total_hours = sum(hours_list)
        total_duration = display_duration(total_hours * 3600)
        data.append(["Total", f"{total_hours:.2f}", total_duration])

        self.add_table(data)
        self.add_pagebreak()

    def _add_employee_shift_tables(self) -> None:
        """
        Adds an employee shift table to the document.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not self.report.shifts.exists():
            return

        employees = (
            Employee.objects.filter(shifts__in=self.report.shifts)
            .distinct()
            .order_by("user__username")
        )
        for employee in employees:
            employee_shifts = self.report.shifts.filter(employee=employee)
            self.add_paragraph(f"Shift Report: {employee}", self.styles["Heading2"])
            self.add_spacer(1, 0.25)
            self._add_employee_weekly_pattern_chart(employee)
            self.add_spacer(1, 0.25)
            data = [["Start Date/Time", "End Date/Time", "Duration"]]
            total_duration = datetime.timedelta(0)

            for shift in employee_shifts:
                start_time = f"{shift.start_datetime:%Y-%m-%d %I:%M %p}"
                end_time = f"{shift.end_datetime:%Y-%m-%d %I:%M %p}"
                duration = shift.get_duration_display()
                data.append([start_time, end_time, duration])
                total_duration += shift.duration

            data.append(["Total", "", display_duration(total_duration.total_seconds())])
            self.add_table(data)
            self.add_spacer(1, 0.5)

            if employee != employees.last():
                self.add_pagebreak()

    def _add_employee_weekly_pattern_chart(self, employee: Employee) -> None:
        """
        Adds an employee weekly shift pattern chart to the document.

        :param employee: An employee.
        :type employee: :py:obj:`~terminusgps_timekeeper.models.Employee`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        shifts = self.report.shifts.filter(employee=employee)
        if not shifts.exists():
            self.add_paragraph(
                f"No shift data available for {employee} in this period.",
                self.styles["Normal"],
            )
            return

        days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        day_totals = {day: 0 for day in days}

        for shift in shifts:
            day_name = shift.start_datetime.strftime("%A")
            hours = shift.duration.total_seconds() / 3600
            day_totals[day_name] += hours

        plt.figure(figsize=(8, 4))
        bars = plt.bar(days, [day_totals[day] for day in days], color="skyblue")
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                plt.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height + 0.1,
                    f"{height:.1f}h",
                    ha="center",
                    va="bottom",
                )
        plt.title(f"Hours Worked by Day of Week: {employee}")
        plt.xlabel("Day of Week")
        plt.ylabel("Total Hours")
        plt.xticks(rotation=45)
        plt.ylim(top=30.0)
        plt.tight_layout()
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format="png", bbox_inches="tight")
        img_buffer.seek(0)
        plt.close()

        self.add_image_buffer(img_buffer, width=7 * units.inch, height=4 * units.inch)
