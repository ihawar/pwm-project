import argparse

from pwm.cli import CliParser
from pwm.storage import  Storage
from pwm.app import app_cli

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


    if args.command == "app":
        app_cli(args, storage)
  