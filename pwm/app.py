from pwm import errors

def app_cli(args, storage):
    if args.action is None:
        print("Here are all apps: {}".format(storage.view_all_apps()))
    
    if args.action == "add":
        try:
            storage.create_app(args.name)
            print("[*] Done.")
        except errors.DataAlreadyExists:
            print("[ERROR] App already exists.")
            
    elif args.action == "delete":
        try:
            storage.delete_app(args.name)
            print("[*] Done.")

        except errors.DataDoesNotExists:
            print("[ERROR] App does not exists.")

    elif args.action == "edit":
        try:
            storage.edit_app(args.name, args.new_name)
            print("[*] Done.")
        
        except errors.DataDoesNotExists:
            print("[ERROR] App does not exists.")
    
    elif args.action == "view":
        try:
            # TODO: here we should add an cool interactive panel.
            print(storage.view_app(args.name))
        except errors.DataDoesNotExists:
            print("[ERROR] App does not exists.")