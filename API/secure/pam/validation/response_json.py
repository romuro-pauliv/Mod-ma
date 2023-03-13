# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                         API.secure.pam.validation.response_json.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.pam.pam_status import Responses
# |--------------------------------------------------------------------------------------------------------------------|

required_fields: list[str] = ["user", "command", "method", "arguments"]

def json_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    if not isinstance(json_md, dict):
        return Responses.R4XX.only_json()
    
    for field in required_fields:
        try:
            if json_md[field]:
                pass
        except KeyError:
            return Responses.R4XX.key_error()
        
    return Responses.R2XX.json_valid()