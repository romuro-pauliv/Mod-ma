# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                  API.secure.base.decrypt_base64.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.responses.base.base64_status import Responses

import base64
import binascii
# |--------------------------------------------------------------------------------------------------------------------|


class Decrypt(object):
    class Base64(object):
        @staticmethod
        # read base64 |================================================================================================|
        def read_authentication(header_credentials: str, _method: str) -> list[str]:
            try:
                try:
                    try:
                        encrypt_credentials: str = header_credentials.split()[1]
                        decrypt_credentials: list[str] = base64.b64decode(encrypt_credentials).decode().split(":")
                        if _method == "login":
                            if len(decrypt_credentials) > 2:
                                return Responses.R4XX.colon_error()
                        if _method == "register":
                            if len(decrypt_credentials) > 3:
                                return Responses.R4XX.colon_not_allowed()
                        if decrypt_credentials[1]:
                            return decrypt_credentials
                    except IndexError:
                        return Responses.R4XX.no_colon_identify()
                except AttributeError:
                    return Responses.R4XX.no_data()
            except binascii.Error:
                return Responses.R4XX.binascii_error()
        # |============================================================================================================|