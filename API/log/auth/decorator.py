# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          API.log.auth.decorator.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.db import get_db

from typing import Any, Callable

import datetime

from flask import request
from functools import wraps
# |--------------------------------------------------------------------------------------------------------------------|

class LogAuth(object):
    def login(func: Callable[..., Any]) -> Callable[[None], tuple[str, int]]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable[[None], tuple[str, int]]:
            # | Execute wrapper function |-----------------------------------------------------------------------------|
            val: Callable[[None], tuple[str, int]] = func(*args, **kwargs)
            # |--------------------------------------------------------------------------------------------------------|

            # BSON LOG |-----------------------------------------------------------------------------------------------|
            log: dict[str, Any] = {
                "user": "root",
                "date": ["UTC", datetime.datetime.utcnow()],
                "log": {"command": f"{func.__name__}",
                        "addr": request.remote_addr,
                        "response": val[0]["response"] if val[1] != 202 else "SUCCESS",
                        "code": val[1]}               
            }
            # |--------------------------------------------------------------------------------------------------------|

            # INPUT LOG |----------------------------------------------------------------------------------------------|
            get_db().USERS.LOG.insert_one(log)
            # |--------------------------------------------------------------------------------------------------------|
            return val
        return wrapper