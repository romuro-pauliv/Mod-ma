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

# Password Validation |------------------------------------------------------------------------------------------------|
def password_validation(passwd: str) -> tuple[str, int]:
    type_char: list[str] = ['lowercase', 'uppercase', 'digits', 'punctuation']

    count: dict[str, int] = {
        "lowercase": 0,
        "uppercase": 0,
        "digits": 0,
        "punctuation": 0
    }
    
    ascii_base: dict[str] = {
        "lowercase": string.ascii_lowercase,
        "uppercase": string.ascii_uppercase,
        "digits": string.digits,
        "punctuation": string.punctuation
    }

    if len(passwd) >= 8:
        for _char in passwd:
            for tc in type_char:
                if _char in ascii_base[tc]:
                    count[tc] += 1
    else:
        return "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS", HTTP_400_BAD_REQUEST

    for tc in type_char:
        if count[tc] < 1:
            return str("MISSING 1 " + tc.upper() + " CHARACTER"), HTTP_400_BAD_REQUEST
    
    return "PASSWORD VALID", HTTP_202_ACCEPTED
# |--------------------------------------------------------------------------------------------------------------------|

class PassException(Exception):
    pass


def register(email: str, username: str, password: str) -> tuple[str, int]:

    # Password validation |--------------------------------------------------------------------------------------------|
    passwd_valid: tuple[str, int] = password_validation(password)
    if passwd_valid[1] == HTTP_400_BAD_REQUEST:
        return passwd_valid
    # |----------------------------------------------------------------------------------------------------------------|

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