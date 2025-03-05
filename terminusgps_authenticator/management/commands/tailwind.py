import argparse
import json
import os
import pathlib

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class Command(BaseCommand):
    help = "Builds and/or compiles tailwind classes"

    def __init__(self, *args, **kwargs) -> None:
        """
        Ensures necessary settings are set before calling the command.

        :raises ImproperlyConfigured: If :py:confval:`TAILWIND_INPUT` was not set.
        :raises ImproperlyConfigured: If :py:confval:`TAILWIND_OUTPUT` was not set.
        :raises ImproperlyConfigured: If either input or output filepath were invalid.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        super().__init__(*args, **kwargs)
        if not hasattr(settings, "TAILWIND_INPUT"):
            raise ImproperlyConfigured("'TAILWIND_INPUT' setting is required.")
        if not hasattr(settings, "TAILWIND_OUTPUT"):
            raise ImproperlyConfigured("'TAILWIND_OUTPUT' setting is required.")

        try:
            pathlib.Path(settings.TAILWIND_INPUT).resolve()
            pathlib.Path(settings.TAILWIND_OUTPUT).resolve()
        except OSError as e:
            raise ImproperlyConfigured(e)

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Adds subcommand arguments to the ``tailwind`` command.

        +-------------+-------------------------------------------------------------------+
        | Subcommand  | Action                                                            |
        +=============+===================================================================+
        | ``install`` | Installs the tailwind compiler for the project.                   |
        +-------------+-------------------------------------------------------------------+
        | ``build``   | Builds the tailwind output file for production.                   |
        +-------------+-------------------------------------------------------------------+
        | ``start``   | Starts the tailwind compiler. Must be canceled with ``<CTRL>-c``. |
        +-------------+-------------------------------------------------------------------+

        :param parser: An argument parser.
        :type parser: :py:obj:`argparse.ArgumentParser`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.add_parser("install", help="Install tailwind")
        subparsers.add_parser("start", help="Start the tailwind compiler")
        subparsers.add_parser("build", help="Build tailwind for production")

    def handle(self, *args, **options):
        """
        Handles command execution based on the provided subcommand.

        :raises CommandError: If the subcommand is invalid.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        subcommand = options["subcommand"]
        try:
            command = self.generate_command(subcommand)
            os.system(command)
        except ValueError as e:
            raise CommandError(e)

    def generate_command(self, subcommand: str | None) -> str:
        """
        Generates a tailwind command based on the provided subcommand.

        :returns: A command to be executed by :py:func:`os.system`.
        :rtype: :py:obj:`str`
        """
        command = f"npx @tailwindcss/cli -i {settings.TAILWIND_INPUT} -o {settings.TAILWIND_OUTPUT}"
        match subcommand:
            case "start":
                styled = self.style.NOTICE
                message = "Starting tailwind compiler..."
                command += " --watch"
            case "build":
                styled = self.style.NOTICE
                message = "Building tailwind for production..."
                command += " --minify"
            case "install":
                if not self.node_package_installed("tailwindcss"):
                    styled = self.style.NOTICE
                    message = "Installing tailwind..."
                    command = "npm install -D tailwindcss @tailwindcss/cli"
                else:
                    styled = self.style.WARNING
                    message = "Tailwind is already installed, building for production instead..."
                    command += "--minify"
            case _:
                raise ValueError("Invalid subcommand '%(cmd)s'" % {"cmd": subcommand})
        self.stdout.write(styled(message))
        return command

    def get_node_dependencies(self) -> list[str]:
        """
        Retrives a list of application dependencies from ``package.json``.

        Returns an empty list if ``package.json`` does not exist.

        :returns: A list of application dependencies as strings.
        :rtype: :py:obj:`list`

        """
        dependencies: list[str] = []
        if not os.path.isfile("package.json"):
            return dependencies

        with open("package.json", "r") as file:
            dependencies.extend(json.load(file).get("devDependencies").keys())
        return dependencies

    def node_package_installed(self, name: str) -> bool:
        """
        Checks whether or not a node package is installed.

        :returns: Whether or not node package ``name`` is installed.
        :rtype: :py:obj:`bool`

        """
        return name in self.get_node_dependencies()
