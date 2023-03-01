# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                    API.json.reponses.auth.delete_account_status.py |
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
        def incorrect_email(email: str) -> tuple[dict[str], int]:
            return response_structure(f"INCORRECT EMAIL [{email}]", HTTP_400_BAD_REQUEST)
    
    class R2XX(object):
        @staticmethod
        def correct_credentials() -> tuple[dict[str], int]:
            return response_structure("VALIDATED CREDENTIALS - YOUR ACCOUNT WILL BE DELETED", HTTP_202_ACCEPTED)