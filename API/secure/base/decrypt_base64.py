# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  API.secure.base.decrypt_base64.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *

import base64
import binascii
# |--------------------------------------------------------------------------------------------------------------------|


class Decrypt(object):
    class Base64(object):
        @staticmethod
        # read base64 |================================================================================================|
        def read_authentication(header_auth: str, _method: str) -> list[str]:
            try:
                try:
                    try:
                        auth: str = header_auth.split()[1]
                        login_data: list[str] = base64.b64decode(auth).decode().split(":")

                        if _method == "login":
                            if len(login_data) > 2:
                                return "BAD REQUEST - COLON ERROR", HTTP_400_BAD_REQUEST
                        if _method == "register":
                            if len(login_data) > 3:
                                return "CHARACTER [:] NOT ALLOWED", HTTP_400_BAD_REQUEST

                        if login_data[1]:
                            return login_data
                    except IndexError:
                        return "BAD REQUEST - NO COLON IDENTIFY", HTTP_400_BAD_REQUEST
                except AttributeError:
                    return "BAD REQUEST - NO DATA", HTTP_400_BAD_REQUEST
            except binascii.Error:
                return "BAD REQUEST - BINASCII ERROR", HTTP_400_BAD_REQUEST
        # |============================================================================================================|