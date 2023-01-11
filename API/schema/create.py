# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.schema.create.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from typing import Optional
from colorama import Fore, Style
from pymongo.mongo_client import MongoClient

import datetime

from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash
# |--------------------------------------------------------------------------------------------------------------------|

def prompt_database(mode: str, db: str, func: Optional[MongoClient] = None) -> None:
    space: str = " "*(30 - len(db))
    if mode == "create":
        print(">>> " + Fore.CYAN + db + space + Style.RESET_ALL + " |---| ", end="")
        func()[db]
        print(Fore.GREEN + "CREATED" + Style.RESET_ALL)
    
    if mode == "exists":
        print(">>> " + Fore.CYAN + db + space + Style.RESET_ALL + " |---| " 
              + Fore.MAGENTA + "OK" + Style.RESET_ALL)


def prompt_collection(mode: str, coll: str, db: Optional[str] = None, func: Optional[MongoClient] = None) -> None:
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


def prompt_admin_user(mode: str,
                      username: str, passwd: Optional[str] = None,
                      func: Optional[MongoClient] = None) -> None:
    
    space: str = " "*(24-len(username))
    if mode == "create":
        # Assemble package |-------------------------------------------------------------------------------------------|
        id_str: str = str(ObjectId())
        json_package: dict[str, str] = {
            "_id": id_str,
            "user": "root",
            "datetime": ["UTC", datetime.datetime.utcnow()],
            "username": username,
            "password": generate_password_hash(passwd),
            "email": "admin@admin.com"
        }
        # |------------------------------------------------------------------------------------------------------------|
        print(">>> " + Fore.MAGENTA + "USER: " + Fore.CYAN + username + space + Style.RESET_ALL + " |---|", end="")
        func().USERS.REGISTER.insert_one(json_package)
        print(Fore.GREEN + " CREATED" + Style.RESET_ALL)

    if mode == "exists":
        print(">>> " + Fore.MAGENTA + "USER: " + Fore.CYAN + username + space + Style.RESET_ALL + " |---|"
              + Fore.MAGENTA + " OK" + Style.RESET_ALL)


def prompt_assemble_privileges(username: str, func: MongoClient) -> None:
    methods: dict[str, list[str]] = {
        "create": [username],
        "read": [username],
        "update": [username],
        "delete": [username]
    } 

    privileges: dict[str, dict] = {
        "command": "privileges",
        "datetime": ['UTC', datetime.datetime.utcnow()],
        "database": methods,
        "collection": methods,
    }

    space: str = " "*(25-len(username))
    print(">>> " + Fore.MAGENTA + "IAM: " + Fore.CYAN + username + space + Style.RESET_ALL + " |---|", end="")

    for db_name in func().list_database_names():
        if db_name not in ["admin", "local", "config"]:
            privileges[db_name]: dict[str, dict] = {}

            for coll_name in func()[db_name].list_collection_names():
                privileges[db_name][coll_name] = methods
    
    func().USERS.PRIVILEGES.insert_one(privileges)

    print(Fore.GREEN + " CREATED" + Style.RESET_ALL)