import typer
from app import __version__


def show_version(ctx: typer.Context) -> None:
    """
    Display build version
    """

    console = ctx.obj.console
    console.print(f"EasySec {__version__}")
