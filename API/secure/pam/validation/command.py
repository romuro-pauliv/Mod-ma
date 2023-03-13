# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.secure.pam.validation.command.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.pam.pam_status import Responses
from API.models.tools.validations import Validate

from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|

commands_value: list[str] = ["append", "remove"]


def command_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    validate_str: tuple[dict[str], int] = Validate.STRING.str_type(json_md["command"])
    if validate_str[1] != HTTP_202_ACCEPTED:
        return validate_str
    
    if not json_md["command"] in commands_value:
        return Responses.R4XX.invalid_command(json_md["command"])
    
    return Responses.R2XX.command_valid()
