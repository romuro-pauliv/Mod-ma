# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                        API.iam,check_permission.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from functools import wraps
from typing import Callable, Any
from flask import request, g
from pymongo import MongoClient

from API.secure.token.IPT_token import IPToken
from API.json.responses.iam import iam_status
from API.db import get_db
# |--------------------------------------------------------------------------------------------------------------------|


class IAM(object):
    @staticmethod
    def check_permission(method: str, structure: list | str) -> tuple[dict, str] | Callable[..., Any]:
        def inner(func: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(func)
            def wrapper(*args, **kwargs) -> Callable[..., Any]:
                authorization: str  = request.headers.get("Authorization")
                privileges_query: dict[str] = {"command": "privileges"}
                
                structure_type: dict[str] = {"general": ["database", "collection"], "specific": "specific"}
                
                username: str = IPToken.Tools.get_username_per_token(authorization)
                privileges: dict[str, list | dict] = get_db().USERS.PRIVILEGES.find_one(privileges_query)
                
                if structure in structure_type['general']:
                # | General Structure Verification |-------------------------------------------------------------------|
                    if username in privileges[structure][method]:
                        return func(*args, **kwargs)
                    else:
                        return iam_status.Responses.R4XX.require_privileges_error(username)
                # |----------------------------------------------------------------------------------------------------|
                elif structure == structure_type['specific']:
                # | Specific Structure Verification |------------------------------------------------------------------|
                    database: str = request.json['database']
                    collection: str = request.json['collection']
                    
                    if database not in privileges:
                        return iam_status.Responses.R4XX.database_not_found(database)

                    if collection not in privileges[database]:
                        return iam_status.Responses.R4XX.collection_not_found(collection)
                    
                    if username in privileges[database][collection][method]:
                        return func(*args, **kwargs)
                    else:
                        return iam_status.Responses.R4XX.require_privileges_error(username)
                # |----------------------------------------------------------------------------------------------------|
            return wrapper
        return inner