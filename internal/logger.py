from time import strftime
from rich import print

class Logger:
    def __init__(self):
        pass

    def success(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold green][ SUCCESS ][/] [bold white]{text}[/]")
    
    def error(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold red][ ERROR ][/] [bold white]{text}[/]")

    def info(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold blue][ INFO ][/] [bold white]{text}[/]")

    def warning(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold yellow][ WARNING ][/] [bold white]{text}[/]")

    def debug(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold grey][ DEBUG ] {text}[/]")
    
    def question(self, text: str):
        print(f"[bold white][{strftime('%H:%M:%S')}][/][bold cyan][ QUESTION ][/] [bold white]{text}[/]", end = " ")
        return input()
