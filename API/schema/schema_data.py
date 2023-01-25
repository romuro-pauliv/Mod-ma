from typing import Union

schema_db: dict[str, list[str]] = {
    "LOG": ["MAINLOG"],
    "USERS": ["REGISTER", "PRIVILEGES", "LOG"],
    "PERSON": ["LEGAL-PERSON", "NATURAL-PERSON", "LOG"],
    "PRODUCTS": ["SERVICES", "PRODUCTS", "LOG"]
}


new_user_privileges: dict[str, Union[list[str], dict[str, list[str]]]] = {
    "database": ["read"],
    'collection': ['read'],
    "PERSON": {
        "LEGAL-PERSON": ["read"],
        "NATURAL-PERSON": ["read"]
    },
    "PRODUCTS": {
      "SERVICES": ["read"],
      "PRODUCTS": ["read"] 
    }
}