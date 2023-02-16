import requests
import threading
from config import *
from colorama import Fore, Style
import urllib3

def login_function(username: str, password: str) -> str:
    header: dict[str] = {"Authorization": header_base64_register(username, password)}
    return requests.post(f"{root_route}{login_route}", headers=header).status_code

def send_request(request_id: int) -> int:
    try:
        if login_function("admin", "123!Admin") == 202:
            print("REQUEST [" + Fore.CYAN + f"{request_id}" + "] --- " + Fore.GREEN + f"{202}" + Style.RESET_ALL)
        else:
            print("REQUEST [" + Fore.CYAN + f"{request_id}" + "] --- " + Fore.RED + "FAILED" + Style.RESET_ALL)
    except urllib3.exceptions.ProtocolError:
        print("REQUEST [" + Fore.CYAN + f"{request_id}" + "] --- " + Fore.RED + "FAILED" + Style.RESET_ALL)

def send_requests_concurrently(num_requests: int) -> None:
    threads: list = []
    for i in range(0, num_requests):
        t = threading.Thread(target=send_request, args=(i+1,))
        threads.append(t)
        
        t.start()
    
    for t in threads:
        t.join()


send_requests_concurrently(1000)