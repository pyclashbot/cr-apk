"""Main module for the CLI application."""

from cleo.application import Application

from src.commands import BuildCommand, ListCommand

application = Application()
application.add(BuildCommand())
application.add(ListCommand())


def main() -> None:
    """Run the CLI application."""
    application.run()


if __name__ == "__main__":
    main()
