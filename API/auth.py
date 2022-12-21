# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                        API.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# +--------------------------------------------------------------------------------------------------------------------+
from .crud import create, read
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from typing import Union, Any, Callable
from .status import *
from bson.objectid import ObjectId
import datetime
# +--------------------------------------------------------------------------------------------------------------------+

# Validation function to verify if not exists equals values |----------------------------------------------------------|
def search_argument(field: str, value: Any) -> bool:
    document: list = []
    for doc in get_db().USERS.REGISTER.find({field: value}):
        document.append(doc)
    try:
        if document[0][field]:
            return False
    except IndexError:
        return True
# |--------------------------------------------------------------------------------------------------------------------|

class PassException(Exception):
    pass


def register(email: str, username: str, password: str) -> tuple[str, int]:
    
    # Validation in database to verify if not exists the same username or email in datbase |---------------------------|
    fields: list = ['email', 'username']
    values: list = [email, username]
    try:
        for i in range(2):
            if search_argument(fields[i], values[i]) == False:
                raise PassException
    except PassException:
        return "EMAIL OR USERNAME IN USE", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    # Assemble document |----------------------------------------------------------------------------------------------|
    id_str: str = str(ObjectId())
    json_package: dict[str, str] = {
        "_id": id_str,
        "user": "root",
        "datetime": ["UTC", datetime.datetime.utcnow()],
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }
    # |----------------------------------------------------------------------------------------------------------------|
    
    get_db().USERS.REGISTER.insert_one(json_package)    # REGISTER COMPLETE
    return "CREATED", HTTP_201_CREATED