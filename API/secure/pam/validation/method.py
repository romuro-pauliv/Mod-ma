# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                API.secure.pam.validation.method.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.models.tools.validations import Validate
from API.json.responses.pam.pam_status import Responses

from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|


methods_value: list[str] = ["create", "read", "update", "delete"]


def method_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    validate_str: tuple[dict[str], int] = Validate.STRING.str_type(json_md["method"])
    if validate_str[1] != HTTP_202_ACCEPTED:
        return validate_str
    
    if not json_md["method"] in methods_value:
        return Responses.R4XX.invalid_crud_method(json_md['method'])
    
    return Responses.R2XX.crud_method_valid()
