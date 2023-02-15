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
        def read_authentication(header_credentials: str, _method: str) -> list[str]:
            methods: list[str] = ["login", "register"]
            try:
                
                encrypt_credentials: str = header_credentials.split()[1]
                decrypt_credentials: list[str] = base64.b64decode(encrypt_credentials).decode().split(":")
            except (IndexError, AttributeError):
                return Responses.R4XX.invalid_header_data()
            except binascii.Error:
                return Responses.R4XX.binascii_error()
               
            if _method == methods[0] and len(decrypt_credentials) != 2:
                return Responses.R4XX.colon_error()
            
            elif _method == methods[1] and len(decrypt_credentials) != 3:
                return Responses.R4XX.colon_error()
            
            elif decrypt_credentials and (_method in methods):
                for credential in decrypt_credentials:
                    
                    if isinstance(credential, str) and len(credential) > 0:
                        return Responses.R2XX.valid(decrypt_credentials)
                    
                    else:
                        return Responses.R4XX.invalid_argument()
            