from pwm import errors
from pwm.utils import getch
from pwm.storage import Password, Storage
from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

class ViewApp:
    def __init__(self, storage: Storage, console: Console, app_name:str):
        self.storage = storage
        self.console = console
        self.app_name = app_name


    def view_app(self):
        try:
            passwords = self.storage.view_app(self.app_name)
        except errors.DataDoesNotExists:
            self.console.print("[ERROR] App does not exists.", justify="center", style="bold red")
            return
        
        table = Table(title=f" - {self.app_name.capitalize()} - ", 
                    expand=True, 
                    title_style="white bold",
                    box=box.MINIMAL,
                    border_style="cyan",
                    header_style="cyan bold")
        
        table.add_column("Id", justify="left", no_wrap=True, style="purple")
        table.add_column("Email", justify="left", no_wrap=True, style="purple")
        table.add_column("Password", justify="left", no_wrap=True, style="red")

        for password in passwords:
            table.add_row(str(password._id), password.email, password.password)
        
        self.console.print(table, justify="center")
        self.console.print("\nUse these keys:", justify="center", style="white italic")
        self.console.print(Panel("Q | Quite  A| Add password E| Edit password D| Delete password",
                            expand=False),
                            justify="center",
                            style="white bold",
                            end="")
        
        while True:
            ch = getch()
            if ch == b'q':
                break
            elif ch == b'a':
                self.__add_password()
                return self.view_app()
            elif ch == b'e':
                self.__edit_password()
                return self.view_app()
            elif ch == b'd':
                self.__delete_password()
                return self.view_app()
             

    def __add_password(self):
        self.console.print("\nAdd a new password to this app", justify="center", style="white bold")
        email = Prompt.ask(" " * round(self.console.size[0] * 0.3)+ " Email",  default="")
        password = Prompt.ask(" " * round(self.console.size[0] * 0.3)+ " Password", password=True)
        while password == "":
            self.console.print("[!] The password can not be none!", justify="center", style="red italic")
            password = Prompt.ask(" " * round(self.console.size[0] * 0.3)+ " Password", password=True)

        self.storage.create_password(app_name=self.app_name, password=Password(email=email, password=password))


    def __edit_password(self):
        self.console.print("\nEdit a password", justify="center", style="white bold")
        _id = Prompt.ask(" " * round(self.console.size[0] * 0.3)+ " Enter password ID")
        if not _id.isdigit():
            self.console.print("[ERROR] Enter a correct id.", style="red italic", justify="center")
            return self.__edit_password()
        try:
            password = self.storage.view_password(app_name=self.app_name, password_id=int(_id))
            new_email = Prompt.ask(" " * round(self.console.size[0] * 0.3) + " New email", default=password.email)
            new_password = Prompt.ask(" " * round(self.console.size[0] * 0.3) + " New password", password=True, default=password.password)
            while new_password == "":
                self.console.print("[!] The password can not be none!", justify="center", style="red italic")
                new_password = Prompt.ask(" " * round(self.console.size[0] * 0.3) + " New password", password=True, default=password.password)

            self.storage.edit_password(app_name=self.app_name, new_password=Password(_id=password._id,
                                                                        email=new_email,
                                                                        password=new_password))
            return

        except errors.DataDoesNotExists:
            self.console.print("[ERROR] Enter a correct id.", style="red italic", justify="center")
            return self.__edit_password() 


    def __delete_password(self):
        self.console.print("\nDelete a password", justify="center", style="white bold")
        _id = Prompt.ask(" " * round(self.console.size[0] * 0.3)+ " Enter password ID")
        if not _id.isdigit():
            self.console.print("[ERROR] Enter a correct id.", style="red italic", justify="center")
            return self.__delete_password()
        try:
            password = self.storage.view_password(app_name=self.app_name, password_id=int(_id))
            is_sure = Confirm.ask(" " * round(self.console.size[0] * 0.3) + " Are you sure?")
            assert is_sure
            if is_sure:
                self.storage.delete_password(app_name=self.app_name, pass_id=password._id)
            return

        except errors.DataDoesNotExists:
            self.console.print("[ERROR] Enter a correct id.", style="red italic", justify="center")
            return self.__delete_password() 