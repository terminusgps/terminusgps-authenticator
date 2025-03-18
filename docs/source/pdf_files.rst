PDF File Generation
===================

=================================
Generating PDF Files for a report
=================================

Use the top-level functions from :py:mod:`terminusgps_timekeeper.pdf_generators`, e.g. :py:func:`~terminusgps_timekeeper.pdf_generators.generate_report_pdf`.

.. code:: python

   from terminusgps_timekeeper.pdf_generators import generate_report_pdf
   from terminusgps_timekeeper.models import Report

   report = Report.objects.filter().get(pk=1) # Retrieve report
   report = generate_report_pdf(report) # Pass it into the function
   report.pdf is not None # True

=========
Reference
=========

.. autofunction:: terminusgps_timekeeper.pdf_generators.generate_report_pdf

.. autoclass:: terminusgps_timekeeper.pdf_generators.PDFReportGenerator
    :members:
    :autoclasstoc:

