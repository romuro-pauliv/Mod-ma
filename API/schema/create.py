# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.schema.create.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Optional
from colorama import Fore, Style

import datetime
# |--------------------------------------------------------------------------------------------------------------------|

def prompt_database(mode: str, db: str, func: Optional[int] = None) -> None:
    space: str = " "*(30 - len(db))
    if mode == "create":
        print(">>> " + Fore.CYAN + db + space + Style.RESET_ALL + " |---| ", end="")
        func()[db]
        print(Fore.GREEN + "CREATED" + Style.RESET_ALL)
    
    if mode == "exists":
        print(">>> " + Fore.CYAN + db + space + Style.RESET_ALL + " |---| " 
              + Fore.MAGENTA + "OK" + Style.RESET_ALL)


def prompt_collection(mode: str, coll: str, db: Optional[str] = None, func: Optional[int] = None) -> None:
    space: str = " "*(27 - len(coll))
    if mode == "create":
        document: dict[str] = {
        "user": "root",
        "datetime": [datetime.datetime.utcnow(), "UTC"],
        "command": f"I'm {coll} and I'm in the {db} database"
        }
        print("    |> " + Fore.LIGHTYELLOW_EX + coll + space + Style.RESET_ALL + " |---| ", end="")
        func()[db][coll].insert_one(document)
        print(Fore.GREEN + "CREATED" + Style.RESET_ALL)
    
    if mode == "exists":
        print("    |> " + Fore.LIGHTYELLOW_EX + coll + space + Style.RESET_ALL + " |---| "
              + Fore.MAGENTA + "OK" + Style.RESET_ALL)