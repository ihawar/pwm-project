import json
import os

from dataclasses import  asdict

from rich.console import Console
from rich.prompt import Prompt

from pwm.storage import  Storage
from pwm import errors


def export(console: Console, storage: Storage, data_type: str, app_name: str):
    console.print(f"[] Exporting data {f'for App(name={app_name})' if app_name else ''} in {data_type} format...", 
                  justify='center', style="white bold")
    file_path = Prompt.ask(" " * round(console.size[0] * 0.3)+ " Enter path for the file", default='.')

    if app_name:
        try:
            data = {app_name: [asdict(d) for d in storage.view_app(app_name)]}
        except errors.DataAlreadyExists:
            console.print("[ERROR] App does not exists.", justify="center", style="bold red")
            return  
    else:
        data = storage.view_all_apps()
     
    if data_type == 'json':
        try:
            path = __export_json(data, f"{file_path}/PWM_DATA__{app_name if app_name else 'ALL'}.json")
        except FileNotFoundError:
            console.print("[ERROR] File path is not valid.", justify="center", style="bold red")
            return    

    else:  
        try:
            path = __export_txt(data, f"{file_path}/PWM_DATA__{app_name if app_name else 'ALL'}.txt")
        except FileNotFoundError:
            console.print("[ERROR] File path is not valid.", justify="center", style="bold red")
            return    


    console.print(f"\n[+] Your data was successfully saved in {os.path.abspath(path)}", 
                  justify='center', style="green")  
    
    
def __export_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)
    
    return file_path
    

def __export_txt(data: dict, file_path):
    str_data = '\r\r========== PWM(Password manager) ==========\n'
    for app_name, passwords in data.items():
        str_data += f'{app_name.capitalize()}:\n'
        for password in passwords:
            str_data += f"\tEmail: {password['email']}\n\tPassword: {password['password']}\n\n"
        
        str_data += f'{"-" * 50}\n'

    with open(file_path, 'w') as file:
        file.write(str_data)
    
    return file_path

