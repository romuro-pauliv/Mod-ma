# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  API.secure.pam.validation.user.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.models.tools.validations import Validate
from API.json.responses.pam.pam_status import Responses

from API.status import *
from API.db import get_db
# |--------------------------------------------------------------------------------------------------------------------|


def user_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    validate_str: tuple[dict[str], int] = Validate.STRING.str_type(json_md['user'])
    if validate_str[1] != HTTP_202_ACCEPTED:
        return validate_str
    
    validate_character: tuple[dict[str], int] = Validate.STRING.character(json_md['user'])
    if validate_character[1] != HTTP_202_ACCEPTED:
        return validate_character
    
    if get_db().USERS.REGISTER.find_one({"username": json_md['user']}) is None:
        return Responses.R4XX.user_not_found(json_md["user"])
    
    return Responses.R2XX.user_valid()