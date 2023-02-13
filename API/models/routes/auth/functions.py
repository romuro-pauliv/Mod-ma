# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.models.auth.tools.validations.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.models.routes.auth.tools.validations import Validate
from API.status import *

from typing import Callable
# |--------------------------------------------------------------------------------------------------------------------|

class Model(object):
    def __init__(self) -> None:
        self.database_validation = Validate.Database
        
        string_validation = Validate.String()
        self.string_func_list: list[Callable[[str], tuple[dict[str], int]]] = [
            string_validation.username,
            string_validation.password,
            string_validation.email
        ]
        
    def register(self, username: str, password: str, email: str) -> tuple[dict[str], int]:
        func_args: list[str] = [username, password, email]
        
        for n, func in enumerate(self.string_func_list):
            response_validation: tuple[dict[str], int] = func(func_args[n])
            if response_validation[1] != HTTP_202_ACCEPTED:
                return response_validation
        
        valid_credentials: list[str] = [username, email]
        field_names: list[str] = ["username", "email"]
        for n, credential in enumerate(valid_credentials):
            valid_in_database: tuple[str | dict[str], int] = self.database_validation.verify_disponibility_in_database(
                field=field_names[n],
                value=credential
            )
            if valid_in_database[1] != HTTP_202_ACCEPTED:
                return valid_in_database
        return valid_in_database