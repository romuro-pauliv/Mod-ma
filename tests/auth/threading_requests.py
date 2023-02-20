import requests
import threading
from config import *
from colorama import Fore, Style
import urllib3
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

def send_request(request_id: int) -> int:
    try:
        status_code, elapsed = login_function("admin", "123!Admin")
        if status_code == 202:
            log_success(request_id, status_code, elapsed)
    except requests.exceptions.ConnectionError:
        log_failed(request_id)

def send_requests_concurrently(num_requests: int) -> None:
    threads: list = []
    for i in range(0, num_requests):
        t = threading.Thread(target=send_request, args=(i+1,))
        threads.append(t)
        
        t.start()
    
    for t in threads:
        t.join()


send_requests_concurrently(120)