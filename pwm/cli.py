import argparse

class CliParser:
    def __init__(self, parser: argparse.ArgumentParser):
        self.__parser = parser
        self.__subparsers = self.__parser.add_subparsers(dest="command")

    def initialize(self):
        app_parser = self.__subparsers.add_parser(name="app", description="App management")
        app_subparsers = app_parser.add_subparsers(dest="action")
        self.__initialize_app(app_subparsers)

        self.__subparsers.add_parser(name="all", description="View all passwords")

        view_parser = self.__subparsers.add_parser(name="view", description="View an app")
        view_parser.add_argument("app_name", help="App name to view")

        export_parser = self.__subparsers.add_parser(name="export", description="Export all data or an app")
        export_parser.add_argument("--app",  required=False)
        export_parser.add_argument('type', choices=['txt', 'json'])

        view_parser = self.__subparsers.add_parser(name="web", description="View all data or an app in web")
        view_parser.add_argument("--app",  required=False)

    
    def __initialize_app(self, app_subparsers):
        add_parser = app_subparsers.add_parser("create", help="Create an app")
        add_parser.add_argument("name", help="App name")

        del_parser = app_subparsers.add_parser("delete", help="Delete an app")
        del_parser.add_argument("name", help="App name")

        edit_parser = app_subparsers.add_parser("edit", help="Edit (rename) an app")
        edit_parser.add_argument("name", help="Old app name")
        edit_parser.add_argument("new_name", help="New app name")
