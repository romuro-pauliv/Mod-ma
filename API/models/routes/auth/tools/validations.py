# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.models.auth.tools.validations.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.auth.register_status import Responses as register_responses

from re import fullmatch
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