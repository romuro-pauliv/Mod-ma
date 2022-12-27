# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                          API.db.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *

from flask import current_app, g
from pymongo import MongoClient
from typing import Union, Any
from bson import json_util
import datetime
import json
# |--------------------------------------------------------------------------------------------------------------------|

# DATABASE CLIENT |====================================================================================================|
def get_db() -> MongoClient:
    if 'db' not in g:
        g.db = MongoClient(current_app.config['MONGO_URI'])
    return g.db
# |====================================================================================================================|


"""
Below you will define the database CRUD methods. All database connections will be defined in the module (only register 
and login methods are not defined here)    
"""


class ExceptionPass(Exception):
    pass


def parse_json(data: list | dict) -> dict:
    """
    Convert API receive json to dict type for easily handle
    Args: data (list | dict): Unformated json
    Returns: return: dict data 
    """
    return json.loads(json_util.dumps(data))


def field_validation(document: dict[str, Any]) -> tuple[str, int]:
    """
    Validation of sended json. Server to don't include fields how date, user, and _id.
    Args: document (dict[str, Any]): Dict to validation
    Returns: tuple[str, int]: Description and HTTP code
    """
    denied_fields: list[str] = ["_id", "date", "user"]
    try:
        for field, _ in document.items():
            if field in denied_fields:
                raise ExceptionPass
    except ExceptionPass:
        return "FORBIDDEN", HTTP_403_FORBIDDEN
    return "OK", HTTP_200_OK


class create(object):
    @staticmethod
    def database(name: str) -> tuple[str, int]:
        database_name: str = name.lower()

        # database search |--------------------------------------------------------------------------------------------|
        if database_name in get_db().list_database_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        # Create database |--------------------------------------------------------------------------------------------|
        document: dict[str, str | list] = {
            "user": 'root',
            "datetime": ['UTC', datetime.datetime.utcnow()],
            "command": f"Hello, I'm {database_name}"
        }

        get_db()[database_name].LOG.insert_one(document)
        # |------------------------------------------------------------------------------------------------------------|

        return 'CREATE', HTTP_201_CREATED