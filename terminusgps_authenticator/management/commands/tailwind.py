import argparse
import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Builds and/or compiles tailwind classes"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        """
        Adds subcommand arguments to the ``tailwind`` command.

        +-------------+-------------------------------------------------------------------+
        | Subcommand  | Action                                                            |
        +=============+===================================================================+
        | ``build``   | Builds the tailwind output file for production.                   |
        +-------------+-------------------------------------------------------------------+
        | ``install`` | Installs the tailwind compiler for the project.                   |
        +-------------+-------------------------------------------------------------------+
        | ``start``   | Starts the tailwind compiler. Must be canceled with ``<CTRL>-c``. |
        +-------------+-------------------------------------------------------------------+

        :param parser: An argument parser.
        :type parser: :py:obj:`argparse.ArgumentParser`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        subparsers = parser.add_subparsers(dest="subcommand")
        subparsers.add_parser("build", help="Build tailwind for production")
        subparsers.add_parser("install", help="Install tailwind")
        subparsers.add_parser("start", help="Start the tailwind compiler")

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
        input, output = self.get_input_filepath(), self.get_output_filepath()
        command = f"npx @tailwindcss/cli -i {input} -o {output}"
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

    def get_input_filepath(self) -> str:
        """Returns the first input.css file found in ``BASE_DIR/css``."""
        return "./src/static/src/css/input.css"

    def get_output_filepath(self) -> str:
        """Returns the first output.css file found in ``BASE_DIR/css``."""
        return "./src/static/src/css/output.css"
