from time import strftime
from rich import print

class Logger:
    def __init__(self):
        pass

    def success(self, text: str, start_new: bool = False, end_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold green][ SUCCESS ][/] [bold white]{text}[/]{'\n' if end_new else ''}")
    
    def error(self, text: str, start_new: bool = False, end_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold red][ ERROR ][/] [bold white]{text}[/]{'\n' if end_new else ''}")

    def info(self, text: str, start_new: bool = False, end_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold blue][ INFO ][/] [bold white]{text}[/]{'\n' if end_new else ''}")

    def warning(self, text: str, start_new: bool = False, end_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold yellow][ WARNING ][/] [bold white]{text}[/]{'\n' if end_new else ''}")

    def debug(self, text: str, start_new: bool = False, end_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold grey][ DEBUG ] {text}[/]{'\n' if end_new else ''}")
    
    def question(self, text: str, start_new: bool = False):
        print(f"{'\n' if start_new else ''}[bold white][{strftime('%H:%M:%S')}][/][bold cyan][ QUESTION ][/] [bold white]{text}[/]", end = " ")
        return input()
