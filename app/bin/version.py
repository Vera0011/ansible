import typer
from app.cli import __version__


def show_version(ctx: typer.Context) -> None:
    """
    Display build version
    """

    console = ctx.obj.console
    console.print(f"EasySec {__version__}")
