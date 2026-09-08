from __future__ import annotations
import typer

#from app.bin.audit import audit
from app.gui.app import EasySecApp
#from app.bin.version import show_version
#from app.core.context import Context


#@app.callback()
#def main(ctx: typer.Context) -> None:
#    """
#    This function sets up the context and starts the app
#    """
#
#    context = Context.discover()
#    ctx.obj = context


#app.command(name="version")(show_version)
#app.command(name="audit")(audit)
#app.command(name="harden")(hardening)

if __name__ == "__main__":
    EasySecApp().mainloop()