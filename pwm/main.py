import argparse

from pwm.cli import CliParser
from pwm.storage import  Storage
from pwm.app import app_cli
from rich.console import Console


def main():
    # CLI
    parser = argparse.ArgumentParser(prog="PWM", 
                                     description="A terminal password manager.",
                                     )
    
    cli_parser = CliParser(parser)
    cli_parser.initialize()

    args = parser.parse_args()

    # Storage
    storage = Storage()
    storage.create_file()

    # console
    console = Console()

    console.print("=" * round(console.size[0] * 0.5), style="dim cyan", justify="center")
    console.print("WELCOME TO PWM (Password Manager)", style="bold purple", justify="center")
    console.print("=" * round(console.size[0] * 0.5), style="dim cyan", justify="center")
    
    
    if args.command == "app":
        app_cli(args, storage, console)
