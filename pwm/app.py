from pwm import errors
from rich.console import Console

def app_cli(args, storage, console:Console):
    if args.action is None:
        # TODO: interactive panel
        print("Here are all apps: {}".format(storage.view_all_apps()))
    
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
