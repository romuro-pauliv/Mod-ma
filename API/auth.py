# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                        API.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# +--------------------------------------------------------------------------------------------------------------------+
from werkzeug.security import check_password_hash, generate_password_hash

from .status import *
from .db import get_db
from .validation.register_validation import Register
from .validation.login_validation import Login

from typing import Callable

import datetime
# +--------------------------------------------------------------------------------------------------------------------+


class PassException(Exception):
    pass

# REGISTER |===========================================================================================================|
def register(email: str, username: str, password: str) -> tuple[str, int]:
    # tools |----------------------------------------------------------------------------------------------------------|
    tools = Register
    validation = tools.Validation
    # |----------------------------------------------------------------------------------------------------------------|
    # Username, password, and email validation |-----------------------------------------------------------------------|
    func_list: list[Callable[[str], tuple[str, int]]] = [
        validation.username, validation.password, validation.email
    ]
    func_input: list[str] = [username, password, email]
    for n, func in enumerate(func_list):
        func_validation: tuple[str, int] = func(func_input[n])
        if func_validation[1] == HTTP_400_BAD_REQUEST:
            return func_validation
    # |----------------------------------------------------------------------------------------------------------------|
    # Validation in database to verify if not exists the same username or email in database |--------------------------|
    fields: list = ['email', 'username']
    values: list = [email, username]
    try:
        for i in range(2):
            if tools.search_argument(fields[i], values[i]) == False:
                raise PassException
    except PassException:
        return "EMAIL OR USERNAME IN USE", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    # Assemble document |----------------------------------------------------------------------------------------------|
    json_package: dict[str, str] = {
        "user": "root",
        "datetime": ["UTC", datetime.datetime.utcnow()],
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }
    # |----------------------------------------------------------------------------------------------------------------|
    get_db().USERS.REGISTER.insert_one(json_package)    # REGISTER COMPLETE
    return "CREATED", HTTP_201_CREATED
# |====================================================================================================================|

# LOGIN |==============================================================================================================|
def login(username: str, password: str) -> tuple[str, int]:    
    # find password |--------------------------------------------------------------------------------------------------|
    passwd: tuple[str, int] = Login.find_password(username)
    if passwd[1] == HTTP_403_FORBIDDEN:
        return passwd
    # |----------------------------------------------------------------------------------------------------------------|

    # check password |-------------------------------------------------------------------------------------------------|
    if not check_password_hash(passwd[0], password):
        return "INCORRECT USERNAME/PASSWORD", HTTP_403_FORBIDDEN
    # |----------------------------------------------------------------------------------------------------------------|

    return "SUCCESSFULLY", HTTP_202_ACCEPTED
# |====================================================================================================================|

    