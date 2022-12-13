# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.database.crud.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports +------------------------------------------------------------------------------------------------------------+
from .db import get_db
from .status import *
from typing import Callable, Any
import datetime
# +--------------------------------------------------------------------------------------------------------------------+

def log(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple]]:
    def wrapper(*args, **kwargs) -> Callable[[str], tuple]:
        val = func(*args, **kwargs)

        # BSON LOG |---------------------------------------------------------------------------------------------------|
        log: dict = {
            "user": "root",
            "date": ["UTC", datetime.datetime.utcnow()],
            "command": f"CREATE A {func.__name__.upper()}",
            "name": kwargs['name'].lower(),
            "code": val[1] 
        }
        # |------------------------------------------------------------------------------------------------------------|

        get_db().LOG.MAINLOG.insert_one(log)    # input in LOG database
        return val
    return wrapper

class create(object):
    @log
    @staticmethod
    def database(name: str) -> tuple[str, int]:
        database_name = name.lower()            # lowercase database

        # database search |--------------------------------------------------------------------------------------------|
        if database_name in get_db().list_database_names():
            return "Forbidden", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|
        
        # Create database |--------------------------------------------------------------------------------------------|
        get_db()[database_name]["LOG"].insert_one({
            "user": "root",
            "datetime": ["UTC", datetime.datetime.utcnow()],
            "command": f"Hello, I'm {database_name}",
            })
        # |------------------------------------------------------------------------------------------------------------|

        return "Create", HTTP_201_CREATED