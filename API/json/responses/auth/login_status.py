# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                          API.json.reponses.auth.register_status.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.tools.tools import response_structure
# |--------------------------------------------------------------------------------------------------------------------|


class Responses(object):
    class R4XX(object):
        @staticmethod
        def incorrect_username_or_password() -> tuple[dict[str], int]:
            return response_structure("INCORRECT USERNAME/PASSWORD", HTTP_403_FORBIDDEN)
    
    class R2XX(object):
        @staticmethod
        def successfully_login() -> tuple[dict[str], int]:
            return response_structure("SUCCESSFULLY LOGIN", HTTP_202_ACCEPTED)