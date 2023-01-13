from colorama import Fore, Style

PRT_USER_USERNAME: str = str("|> " + Fore.MAGENTA + "username" + Style.RESET_ALL + ": ")
PRT_USER_PASSWORD: str = str("|> " + Fore.MAGENTA + "password" + Style.RESET_ALL + ": ")


def login_successfully(response: str, status_code: int) -> None:
    line_status_code: str = str("| " +  Fore.GREEN + str(status_code) + Style.RESET_ALL 
    + " |==========================================================|")    
    line: str = "|================================================================|"

    space: str = " "*(len(line) - 3 - len(response))
    print(line_status_code), print("| " + Fore.GREEN + response + space + Style.RESET_ALL + "|"), print(line)


def unsuccessful_login(response: str, status_code: int) -> None:
    line_status_code: str = str("| " +  Fore.RED + str(status_code) + Style.RESET_ALL 
    + " |==========================================================|")    
    line: str = "|================================================================|"

    space: str = " "*(len(line) - 3 - len(response))
    print(line_status_code), print("| " + Fore.RED + response + space + Style.RESET_ALL + "|"), print(line)