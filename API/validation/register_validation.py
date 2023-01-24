# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  validation.register_validation.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.db import get_db
from API.status import *

from typing import Any
from re import fullmatch

import string
# |--------------------------------------------------------------------------------------------------------------------|

class Register(object):
    # | Validation function to verify if not exists equals values |====================================================|
    @staticmethod
    def search_argument(field: str, value: Any) -> bool:
        document: list = []
        for doc in get_db().USERS.REGISTER.find({field: value}):
            document.append(doc)
        try:
            if document[0][field]:
                return False
        except IndexError:
            return True
    # |================================================================================================================|
    class Validation(object):
        # | Password Validation |======================================================================================|
        @staticmethod
        def password(passwd: str) -> tuple[str, int]:
            type_char: list[str] = ['lowercase', 'uppercase', 'digits', 'punctuation']

            count: dict[str, int] = {
                "lowercase": 0,
                "uppercase": 0,
                "digits": 0,
                "punctuation": 0
            }
    
            ascii_base: dict[str] = {
                "lowercase": string.ascii_lowercase,
                "uppercase": string.ascii_uppercase,
                "digits": string.digits,
                "punctuation": string.punctuation
            }

            if len(passwd) >= 8:
                for _char in passwd:
                    for tc in type_char:
                        if _char in ascii_base[tc]:
                            count[tc] += 1
            else:
                return "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS", HTTP_400_BAD_REQUEST

            for tc in type_char:
                if count[tc] < 1:
                    return str("MISSING 1 " + tc.upper() + " CHARACTER"), HTTP_400_BAD_REQUEST

            return "PASSWORD VALID", HTTP_202_ACCEPTED
        # |============================================================================================================|
    
        # | Username validation |======================================================================================|
        @staticmethod
        def username(username: str) -> tuple[str, int]:
            if len(username) >= 4:
                for _char in username:
                    if _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
                        return str("CHARACTER [" + _char +  "] NOT ALLOWED"), HTTP_400_BAD_REQUEST
            else:
                return "YOUR USERNAME MUST BE MORE THAN 4 CHARACTERS", HTTP_400_BAD_REQUEST
            return "USERNAME VALID", HTTP_202_ACCEPTED
        # |============================================================================================================|
        
        # | Email validation |=========================================================================================|
        @staticmethod
        def email(email: str) -> tuple[str, int]:
            regex: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            return ("VALID EMAIL", HTTP_202_ACCEPTED) if fullmatch(regex, email) \
                   else ("INVALID EMAIL", HTTP_400_BAD_REQUEST)
        # |============================================================================================================|