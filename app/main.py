from __future__ import annotations
import typer

from app.cli.bin.audit import audit
from app.cli.bin.hardening import hardening
from app.cli.bin.version import show_version
from app.cli.core.context import Context

app = typer.Typer(
    name="easysec",
    help="EasySec — Open source security automation",
    no_args_is_help=True,
    add_completion=False,
    rich_markup_mode="rich",
    epilog="Run 'easysec COMMAND --help' for details on a specific command",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.callback()
def main(ctx: typer.Context) -> None:
    """
    This function sets up the context and starts the app
    """

    context = Context.discover()
    ctx.obj = context


app.command(name="version")(show_version)
app.command(name="audit")(audit)
#app.command(name="harden")(hardening)

if __name__ == "__main__":
    app()
