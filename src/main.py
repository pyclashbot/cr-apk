"""Main module for the CLI application."""

from cleo.application import Application

from src.commands import BuildCommand, ListCommand, PullCommand

application = Application()
application.add(PullCommand())
application.add(ListCommand())
application.add(BuildCommand())


def main() -> None:
    """Run the CLI application."""
    application.run()


if __name__ == "__main__":
    main()
