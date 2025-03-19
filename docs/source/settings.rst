Settings
========

.. confval:: ADMINS

    A sequence of tuples containing an admin name and email address.

    These email addresses recieve Django notifications.

    .. code:: python

        ADMINS = [
            ("Blake", "blake@terminusgps.com"),
            ("Peter", "peter@terminusgps.com"),
            ("Lili", "lili@terminusgps.com"),
        ] 

.. confval:: WIALON_TOKEN

    A Wialon API token.

    .. code:: python

        WIALON_TOKEN = "<YOUR_WIALON_API_TOKEN>"

.. confval:: WIALON_ADMIN_ID

    A Wialon admin user id.

    Wialon API sessions operate as this user by default.

    .. code:: python

        WIALON_ADMIN_ID = "<YOUR_WIALON_ADMIN_ID>"

.. confval:: FIELD_ENCRYPTION_KEY

    A Fernet encryption key for encrypting specific model fields.

    .. code:: python

        FIELD_ENCRYPTION_KEY = "<YOUR_FIELD_ENCRYPTION_KEY>"

.. confval:: TIMEKEEPER_REPO_URL

    A link to the GitHub repository for the timekeeper application.

    .. code:: python

        TIMEKEEPER_REPO_URL = "https://github.com/terminusgps/terminusgps-timekeeper"

.. confval:: FILE_UPLOAD_PERMISSIONS

    Must allow Django to read and write files for pdf file generation.

    .. code:: python

        import stat
        FILE_UPLOAD_PERMISSIONS = stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP

.. confval:: DOCS_ROOT

    Relative path to the docs index.html file.

    .. code:: python

        DOCS_ROOT = BASE_DIR.parent / "docs" / "build" / "html"
