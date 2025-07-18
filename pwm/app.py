from pwm import errors
from rich.console import Console
from rich.table import Table
from rich import box

def app_cli(args, storage, console:Console):
    if args.action == "create":
        try:
            storage.create_app(args.name)
            console.print(f"[+] New App(name={args.name}) created", justify="center", style="bold green")
        except errors.DataAlreadyExists:
            console.print("[ERROR] App already exists.", justify="center", style="bold red")
            
    elif args.action == "delete":
        try:
            storage.delete_app(args.name)
            console.print(f"[-] App(name={args.name}) deleted", justify="center", style="bold red")
        except errors.DataDoesNotExists:
            console.print("[ERROR] App does not exists.", justify="center", style="bold red")

    elif args.action == "edit":
        try:
            storage.edit_app(args.name, args.new_name)
            console.print(f"[!] App(name={args.name}) was changed to App(name={args.new_name})", justify="center", style="bold white")
        
        except errors.DataDoesNotExists:
            console.print("[ERROR] App does not exists.", justify="center", style="bold red")
    
    elif args.action == "view":
        try:
            # TODO: here we should add an cool interactive panel.
            print(storage.view_app(args.name))
        except errors.DataDoesNotExists:
            console.print("[ERROR] App does not exists.", justify="center", style="bold red")


def view_all_apps(storage) -> Table:
    data: dict = storage.view_all_apps()

    table = Table(title=" - All Apps - ", 
                  expand=True, 
                  title_style="white bold",
                  box=box.MINIMAL,
                  border_style="cyan",
                  header_style="cyan bold")

    table.add_column("Name", justify="left", style="purple")
    table.add_column("Email", justify="left", no_wrap=True, style="purple")
    table.add_column("Password", justify="left", no_wrap=True, style="red")
    for app in data.keys():
        for password in data[app]:
            table.add_row(app.capitalize(), password['email'], password['password'])
        table.add_section()
    return table

