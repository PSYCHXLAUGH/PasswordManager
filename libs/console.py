from colorama import init, Fore
from prettytable import PrettyTable
from cowpy import cow

class ConsoleLog:

    def __init__(self):

        init(autoreset = True)
        
        self.STATUS = {

            "+": "[+]",
            "!": "[-]",
            "?": "[?]",
            "!?": "[WARNING]",
            "I": "[INFO]"
            
            }
    
    def error(self, message):
        
        return Fore.RED + self.STATUS["!"] + Fore.WHITE + " " + message

    def ok(self, message):
        
        return Fore.GREEN + self.STATUS["+"] + Fore.WHITE + " " + message
    
    def question(self, message):
        
        return Fore.YELLOW + self.STATUS["?"] + Fore.WHITE + " " + message

    def warning(self, message):
        
        return Fore.YELLOW + self.STATUS["!?"] + Fore.WHITE + " " + message

    def info(self, message):
        
        return Fore.YELLOW + self.STATUS["I"] + Fore.WHITE + " " + message
    
    def date(self, info, time, version):
        
        return Fore.GREEN + cow.milk_random_cow(
            "Author: github.com/PSYCHXLAUGH\n" + "Password Manager " + version + "\nlast update file -> " + str(info) + ", " + str(time) + ""
        )

    def password(self, data):
        
        table = PrettyTable()
        
        table.field_names = data[0]
        table.add_row(data[1])

        return Fore.WHITE + str(table)