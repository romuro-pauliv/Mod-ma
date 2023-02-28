import requests
import threading
from config import *
from colorama import Fore, Style
from random import randint
from datetime import timedelta

def login_function(username: str, password: str) -> str:
    header: dict[str] = {"Authorization": header_base64_login(username, password)}
    response: requests.models.Response = requests.post(f"{root_route}{login_route}", headers=header)
    return response.status_code, response.elapsed

def space_format(string_: str, legth_space: int) -> str:
    return " "*(legth_space - len(string_))

def log_success(request_id: int, status_code: int, elapsed: timedelta) -> None:
    print("REQUEST " + Fore.CYAN + f"[{request_id}]" + space_format(str(request_id), 6) + Style.RESET_ALL + " |---| "
          + Fore.GREEN + f"[{status_code}]" + Style.RESET_ALL + " |---| "
          + "ELAPSED " + Fore.MAGENTA + f"[{round(timedelta.total_seconds(elapsed), 2)}]" + Style.RESET_ALL)

def log_failed(request_id: int) -> str:
    print("REQUEST " + Fore.CYAN + f"[{request_id}]" + space_format(str(request_id), 6) + Style.RESET_ALL + " |---| "
          + Fore.RED + "FAILED" + Style.RESET_ALL)

def turn(qnt_request: int) -> None:
    print(Fore.CYAN + "|-------------------------------------------------------------------------------------------|")
    print("| " + Style.RESET_ALL + "REQUEST TURN: " + Fore.MAGENTA + f"[{qnt_request}]" + Style.RESET_ALL)
    print(Fore.CYAN + "|-------------------------------------------------------------------------------------------|")
    print(Style.RESET_ALL)

def send_request(request_id: int) -> int:
    try:
        status_code, elapsed = login_function("admin", "123!Admin")
        if status_code == 202:
            log_success(request_id, status_code, elapsed)
    except requests.exceptions.ConnectionError:
        log_failed(request_id)

def send_requests_concurrently() -> None:
    while True:
        request_qnt: int = randint(1, 40)
        turn(request_qnt)
        threads: list = []
        for i in range(0, request_qnt):
            t = threading.Thread(target=send_request, args=(i+1,))
            threads.append(t)
        
            t.start()
    
        for t in threads:
            t.join()


send_requests_concurrently()