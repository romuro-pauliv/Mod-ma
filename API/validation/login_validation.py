# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                     validation.login_validation.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import get_db
# |--------------------------------------------------------------------------------------------------------------------|

class Login(object):
    # | Find password |================================================================================================|
    @staticmethod
    def find_password(username: str) -> tuple[str, int]:
        document: list = []
        for doc in get_db().USERS.REGISTER.find({"username": username}):
            document.append(doc)
        try:
            if document[0]:
                return document[0]['password'], HTTP_200_OK
        except IndexError:
            return "INCORRECT USERNAME/PASSWORD", HTTP_403_FORBIDDEN
    # |================================================================================================================|
    class Validation(object):
        pass