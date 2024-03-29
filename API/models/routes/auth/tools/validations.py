# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.models.auth.tools.validations.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.auth.register_status import Responses as register_responses
from API.json.responses.auth.login_status import Responses as login_responses
from API.json.responses.auth.delete_account_status import Responses as delete_account_responses
from API.db import get_db

from werkzeug.security import check_password_hash
from re import fullmatch
from typing import Any
import string
# |--------------------------------------------------------------------------------------------------------------------|


class Validate(object):
    class String(object):
        def __init__(self) -> None:
            self.forbidden_char: str = "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c"
            self.regex_email: str = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            
            self.count_char: dict[str, int] = {
                "lowercase": 0, "uppercase": 0, "digits": 0, "punctuation": 0
            }
            self.ascii_base: dict[str] = {
                "lowercase": string.ascii_lowercase, "uppercase": string.ascii_uppercase,
                "digits": string.digits, "punctuation": string.punctuation
            }
            
            self.type_ascii: list[str] = [
                "lowercase", "uppercase", "digits", "punctuation"
            ]
            
        def username(self, username: str) -> tuple[dict[str] | str, int]:
            if len(username) >= 4:
                for _char in username:
                    if _char in self.forbidden_char:
                        return register_responses.Username.R4XX.character_not_allowed(_char)
            else:
                return register_responses.Username.R4XX.more_than_4_characters(username)
            return register_responses.Username.R2XX.valid_username()
        
        def email(self, email: str) -> tuple[dict[str] | str, int]:
            return register_responses.Email.R2XX.valid_email() if fullmatch(self.regex_email, email) \
                else register_responses.Email.R4XX.invalid_email(email)
        
        def password(self, password: str) -> tuple[dict[str] | str, int]:
            if len(password) >= 8:
                for _char in password:
                    for char_mode in self.type_ascii:
                        if _char in self.ascii_base[char_mode]:
                            self.count_char[char_mode] += 1
            else:
                return register_responses.Password.R4XX.more_than_8_characters()
            
            for char_mode in self.type_ascii:
                if self.count_char[char_mode] < 1:
                    return register_responses.Password.R4XX.missing_one_character(char_mode)
            
            return register_responses.Password.R2XX.valid_password()
    
    class Database(object):
        @staticmethod
        def verify_disponibility_in_database(field: str, value: str) -> tuple[dict[str], int]:
            document: dict[str, Any] = get_db().USERS.REGISTER.find_one({field: value})
            try:
                if document[field]:
                    return register_responses.DatabaseSearch.R4XX.email_or_username_in_use()
            except TypeError:
                return register_responses.DatabaseSearch.R2XX.available()
        
        @staticmethod
        def verify_password(username: str, password: str) -> tuple[dict[str], int]:
            document: dict[str] = get_db().USERS.REGISTER.find_one({"username": username})
            try:
                True if document["username"] else False
            except TypeError:
                return login_responses.R4XX.incorrect_username_or_password()
            
            if not check_password_hash(document["password"], password):
                return login_responses.R4XX.incorrect_username_or_password()
            
            return login_responses.R2XX.successfully_login()
        
        @staticmethod
        def verify_email(username: str, email: str) -> tuple[dict[str], int]:
            document: dict[str] = get_db().USERS.REGISTER.find_one({"username": username})
            try:
                True if document["username"] else False
            except TypeError:
                return login_responses.R4XX.incorrect_username_or_password()
            
            if document['email'] != email:
                return delete_account_responses.R4XX.incorrect_email(email)
            
            return delete_account_responses.R2XX.correct_credentials()