# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           CLI.command.auth.auth.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import base64
# |--------------------------------------------------------------------------------------------------------------------|


def header_base64_login(username: str, password: str) -> str:
    encode_pass: bytes = f'{username}:{password}'.encode()
    return f"Basic {base64.b64encode(encode_pass).decode()}"


def header_base64_register(username: str, password: str, email: str) -> str:
    encode_register: bytes = f"{username}:{password}:{email}".encode()
    return f"Basic {base64.b64encode(encode_register).decode()}"