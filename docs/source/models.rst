Models
======

=========
Employees
=========

Employees are Django database models that store user information.

.. autoclass:: terminusgps_timekeeper.models.Employee
    :members:
    :autoclasstoc:

===========
Punch Cards
===========

All employees have a punch card object that creates shifts on a punch out.

.. autoclass:: terminusgps_timekeeper.models.EmployeePunchCard
    :members:
    :autoclasstoc:

======
Shifts
======

A shift object is created when a punch card is punched out successfully.

.. autoclass:: terminusgps_timekeeper.models.EmployeeShift
    :members:
    :autoclasstoc:

=======
Reports
=======

Reports are generated programatically at different time intervals. This is configurable in the Django settings module.

.. autoclass:: terminusgps_timekeeper.models.Report
    :members:
    :autoclasstoc:
