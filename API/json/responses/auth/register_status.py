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
    class Username(object):
        class R4XX(object):
            @staticmethod
            def character_not_allowed(_char: str) -> tuple[dict[str], int]:
                return response_structure(f"CHARACTER [{_char}] NOT ALLOWED", HTTP_400_BAD_REQUEST)
            
            @staticmethod
            def more_than_4_characters(username: str) -> tuple[dict[str], int]:
                return response_structure(f"THE USERNAME [{username}] NEED MORE THAN 4 CHARACTERS",
                                          HTTP_400_BAD_REQUEST)

        class R2XX(object):
            @staticmethod
            def valid_username() -> tuple[str, int]:
                return "USERNAME IS VALID", HTTP_202_ACCEPTED
    
    class Email(object):
        class R4XX(object):
            @staticmethod
            def invalid_email(email: str) -> tuple[dict[str], int]:
                return response_structure(f"EMAIL [{email}] INVALID", HTTP_400_BAD_REQUEST)
        
        class R2XX(object):
            @staticmethod
            def valid_email() -> tuple[str, int]:
                return "VALID EMAIL", HTTP_202_ACCEPTED
    
    class Password(object):
        class R4XX(object):
            @staticmethod
            def more_than_8_characters() -> tuple[dict[str], int]:
                return response_structure("YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS", HTTP_400_BAD_REQUEST)

            @staticmethod
            def missing_one_character(_char: str) -> tuple[dict[str], int]:
                return response_structure(f"MISSING 1 [{_char.upper()}] CHARACTER", HTTP_400_BAD_REQUEST)
            
        class R2XX(object):
            @staticmethod
            def valid_password() -> tuple[str, int]:
                return "PASSWORD VALID", HTTP_202_ACCEPTED
    
    class DatabaseSearch(object):
        class R4XX(object):
            @staticmethod
            def email_or_username_in_use() -> tuple[dict[str], int]:
                return response_structure("EMAIL OR USERNAME IN USE", HTTP_403_FORBIDDEN)
        
        class R2XX(object):
            @staticmethod
            def available() -> tuple[str, int]:
                return "AVAILABLE TO REGISTER", HTTP_202_ACCEPTED
    
    class ExecRegister(object):
        class R2XX(object):
            @staticmethod
            def successfully_registered() -> tuple[dict[str], int]:
                return response_structure("SUCCESSFULLY REGISTERED", HTTP_201_CREATED)