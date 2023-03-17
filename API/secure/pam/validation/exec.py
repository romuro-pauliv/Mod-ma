# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  API.secure.pam.validation.exec.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.secure.pam.validation.response_json import json_validation
from API.secure.pam.validation.user import user_validation
from API.secure.pam.validation.command import command_validation
from API.secure.pam.validation.method import method_validation
from API.secure.pam.validation.arguments import arguments_validation

from typing import Callable
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|


def execute_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    func_validation_list: list[Callable[[dict[str]], tuple[dict[str], int]]] = [
        json_validation,
        user_validation,
        command_validation,
        method_validation,
        arguments_validation
    ]
    
    for func_validation in func_validation_list:
        validation_response: tuple[dict[str], int] = func_validation(json_md)
        if validation_response[1] != HTTP_202_ACCEPTED:
            return validation_response
    
    return json_md, HTTP_202_ACCEPTED
