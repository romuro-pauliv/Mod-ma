# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                         API.iam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from .db import get_db
from .auth import get_username_per_token
from .status import *

from flask import request
from typing import Callable, Any, Union
from functools import wraps
# |--------------------------------------------------------------------------------------------------------------------|


class IAM(object):
    @staticmethod
    def check_permission(method: str, structure: list | str) -> Callable:
        
        def inner(func: Callable[..., Any]) -> Callable:
            @wraps(func)
            def involved(*args, **kwargs) -> Callable[..., Any]:
                # GET USERNAME |---------------------------------------------------------------------------------------|
                username: str = get_username_per_token(request.headers.get("Authorization"))
                # |----------------------------------------------------------------------------------------------------|

                # REQUEST THE PRIVILEGES DATA |------------------------------------------------------------------------|
                privileges: dict = get_db().USERS.PRIVILEGES.find_one({"username": username})
                # |----------------------------------------------------------------------------------------------------|

                if isinstance(structure, str):
                    if structure in ["database", "collection", "document"]:
                        if privileges[structure][method]:
                            return func(*args, **kwargs)
                        else:
                            return "REQUIRE PRIVILEGES", HTTP_403_FORBIDDEN
                    else:
                        return "BAD REQUEST - STRUCTURE", HTTP_400_BAD_REQUEST
                else:
                    if len(structure) == 2:
                        if privileges[structure[0]][structure[1]][method]:
                            return func(*args, **kwargs)
                    else:
                        return "BAD REQUEST - STRUCTURE", HTTP_400_BAD_REQUEST
                return "BAD REQUEST", HTTP_400_BAD_REQUEST
            
            involved.__name__ == func.__name__
            return involved
        return inner