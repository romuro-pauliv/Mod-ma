# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                          API.json.auth.register.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import datetime
from werkzeug.security import generate_password_hash
# |--------------------------------------------------------------------------------------------------------------------|

def new_user(username: str, password: str, email: str) -> dict[str | list[str]]:
    json_register: dict[str | list[str]] = {
        "user": "root",
        "datetime": ["UTC", datetime.datetime.utcnow()],
        "username": username,
        "password": generate_password_hash(password),
        "email": email
    }
    return json_register