import argparse
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from pwm.cli import CliParser
from pwm.export import export
from pwm.storage import  Storage
from pwm.app import app_cli, view_all_apps

from pwm.utils import get_data_path
from pwm.view import ViewApp
from pwm.web import view_web


def intro_screen(console: Console):
    
    description = Text("Simple. Offline. Yours.\nNo cloud. No sync. Just pure local passwords.", justify="center")
    description.stylize("italic cyan")

    table = Table.grid(padding=1)
    table.add_column(style="bold green", justify="left")
    table.add_column()
    table.add_row("pwm app create", "Create a new app entry")
    table.add_row("pwm all", "List all apps with passwords")
    table.add_row("pwm view <name>", "View am app")
    table.add_row("pwm web", "Open web UI")
    table.add_row("pwm export", "Export data")

    tip = Panel.fit("Tip: Start with [bold]pwm app create <app name>[/bold] to add your first password.", style="dim")

    console.print(description, justify='center')
    console.rule("[bold white] Commands: ", style="white")
    console.print(table, justify='center')
    console.print(tip, justify='center')


def main():
    # CLI
    parser = argparse.ArgumentParser(prog="PWM", 
                                     description="A terminal password manager.",
                                     )
    
    cli_parser = CliParser(parser)
    cli_parser.initialize()

    args = parser.parse_args()
    
    # Storage
    storage = Storage(path=Path(get_data_path()) / "storage.pwm")
    storage.create_file()

    # console
    console = Console()

    console.print("=" * round(console.size[0] * 0.5), style="dim cyan", justify="center")
    console.print("PWM - Password Manager", style="bold purple", justify="center")
    console.print("=" * round(console.size[0] * 0.5), style="dim cyan", justify="center")
    
    if args.command == "app":
        app_cli(args, storage, console)
    elif args.command =="all":
        console.print(view_all_apps(storage), justify="center")
    elif args.command == "view":
        ViewApp(storage, console, args.app_name).view_app()
    elif args.command == "export":
        export(console,  storage, data_type=args.type, app_name=args.app)
    elif args.command == "web":
        view_web(console,  storage, app_name=args.app)
    else:
        intro_screen(console)

