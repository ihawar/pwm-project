from dataclasses import dataclass, asdict
import os
import json
import random
from string import digits
from pwm.errors import DataAlreadyExists, DataDoesNotExists


@dataclass
class Password:
    password: str
    _id: int | None = None
    email: str = ""


class Storage:
    def __init__(self, path: str="storage.json"):
        self.file_path: str = path
        self.data: dict = {}

    def create_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        else:
            with open(self.file_path, 'w') as file:
                json.dump(self.data, file, indent=2)

    def __update_file(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=2)


    def create_app(self, name: str):
        if self.data.get(name) is None:
            self.data[name] = []
            self.__update_file()
        else:
            raise DataAlreadyExists(f"App name {name} already exists.")

    def delete_app(self, name: str):
        if self.data.get(name) is None:
            raise DataDoesNotExists(f"App name {name} does not exists.")
        else:
            self.data.__delitem__(name)
            self.__update_file()

    def edit_app(self, name: str, new_name: str):
        if self.data.get(name) is None:
            raise DataDoesNotExists(f"App name {name} does not exists.")
        else:
            self.data[new_name] = self.data.pop(name)
            self.__update_file()
    
    def view_app(self, name: str) -> list[Password]:
        if self.data.get(name) is None:
            raise DataDoesNotExists(f"App name {name} does not exists.")
        else:
            return [Password(**password) for password in self.data[name]]
    
    def view_all_apps(self):
        return self.data

    def create_password(self, app_name: str, password: Password):
        if self.data.get(app_name) is None:
            raise DataDoesNotExists(f"App name {app_name} does not exists.")
        else:
            password._id = int(''.join([random.choice(list(digits)) for _ in range(0, 4)]))
            self.data[app_name].append(asdict(password))
            self.__update_file()

    def delete_password(self, app_name: str, pass_id: int):
        if self.data.get(app_name) is None:
            raise DataDoesNotExists(f"App name {app_name} does not exists.")
        else:
            for password in self.data[app_name]:
                if password["_id"] == pass_id:
                    self.data[app_name].remove(password)
                    self.__update_file()
                    return
            else:
                raise DataDoesNotExists(f"Password with id={pass_id} does not exists in app {app_name}")
    
    def edit_password(self, app_name:str, new_password: Password):
        if self.data.get(app_name) is None:
            raise DataDoesNotExists(f"App name {app_name} does not exists.")
        else:
            for i, password in enumerate(self.data[app_name]):
                if password["_id"] == new_password._id:
                    self.data[app_name][i] = asdict(new_password)
                    self.__update_file()
                    return
            else:
                raise DataDoesNotExists(f"Password with id={new_password._id} does not exists in app {app_name}")
    
    def view_password(self, app_name: str, password_id: int):
        for password in self.view_app(app_name):
            if password._id == int(password_id):
                return password
        else:
            raise DataDoesNotExists(f"Password with id={password} does not exists in app {app_name}")
