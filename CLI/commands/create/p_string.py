# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     CLI.command.create.p_string.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from colorama import Fore, Style
import json
# |--------------------------------------------------------------------------------------------------------------------|

PRT_USER_DATABASE: str = str("|> " + Fore.CYAN + "  database" + Style.RESET_ALL + ": ")
PRT_USER_COLLECTION: str = str("|> " + Fore.CYAN + "collection" + Style.RESET_ALL + ": ")
PRT_USER_DOCUMENT: str = str("|> " + Fore.CYAN + "  document" + Style.RESET_ALL + ": ")

partial_line: str = " |==========================================================|"
line: str = "|================================================================|"



def connection_error() -> None:
    line_status_code: str = str("| " +  Fore.RED + 'NET' + Style.RESET_ALL + partial_line)    
    
    response: str = "CHECK YOUR INTERNET CONNECTION OR MODMA URL"
    space: str = " "*(len(line) - 3 - len(response))

    print(line_status_code), print("| " + Fore.RED + response + space + Style.RESET_ALL + "|"), print(line)


def unsuccessful(response: str, status_code: int) -> None:
    line_status_code: str = str("| " +  Fore.RED + str(status_code) + Style.RESET_ALL + partial_line)    

    space: str = " "*(len(line) - 3 - len(response))
    print(line_status_code), print("| " + Fore.RED + response + space + Style.RESET_ALL + "|"), print(line)


def successfully(response: str, status_code: int) -> None:
    line_status_code: str = str("| " +  Fore.GREEN + str(status_code) + Style.RESET_ALL + partial_line)    
    
    space: str = " "*(len(line) - 3 - len(response))
    print(line_status_code), print("| " + Fore.GREEN + response + space + Style.RESET_ALL + "|"), print(line)