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
        if func.__name__ != "database":
            get_db()[kwargs['database']]['LOG'].insert_one(log)

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
    
    @log
    @staticmethod
    def collection(database: str, name: str) -> tuple[str, int]:
        database_name = database.lower()        # lowercase database
        collection_name = name.lower()          # lowercase collection

        # datbase and collection search |------------------------------------------------------------------------------|
        if database_name not in get_db().list_database_names():
            return "Forbidden", HTTP_403_FORBIDDEN
        
        if collection_name in get_db()[database_name].list_collection_names():
            return "Forbidden", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        # Create collection |------------------------------------------------------------------------------------------|
        get_db()[database_name][collection_name].insert_one({
            "user": "root",
            "datetime": ["UTC", datetime.datetime.utcnow()],
            "command": f"Hello, I'm {collection_name}",
        })
        # |------------------------------------------------------------------------------------------------------------|

        return "Create", HTTP_201_CREATED
