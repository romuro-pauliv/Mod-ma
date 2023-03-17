# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                             API.secure.pam.validation.arguments.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from API.json.responses.pam.pam_status import Responses

from API.status import *
from API.db import get_db
# |--------------------------------------------------------------------------------------------------------------------|


def get_privileges() -> dict[str, dict[str]]:
    remove_fields: list[str] = ["_id", "command", "datetime"]
    privileges: dict[str] = get_db().USERS.PRIVILEGES.find_one({"command": "privileges"})
    
    for rf in remove_fields:
        del privileges[rf]
    
    return privileges


def arguments_validation(json_md: dict[str]) -> tuple[dict[str], int]:
    if not isinstance(json_md["arguments"], list):
        return Responses.R4XX.invalid_object_type_arguments()
    
    for arg_l in json_md["arguments"]:
        if not isinstance(arg_l, str):
            if not isinstance(arg_l, list):
                return Responses.R4XX.invalid_item_in_arguments(arg_l)
    
    for arg_l in json_md["arguments"]:
        if isinstance(arg_l, str):
            if not arg_l in ["database", "collection"]:
                return Responses.R4XX.invalid_path(arg_l)
        
        if isinstance(arg_l, list):
            if len(arg_l) > 2 or len(arg_l) < 2:
                return Responses.R4XX.invalid_path_error_len_list(arg_l)

            for item_l in arg_l:
                if not isinstance(item_l, str):
                    return Responses.R4XX.invalid_item_in_list(item_l)
                
            privileges: dict[str, dict[str]] = get_privileges()
            del privileges["database"], privileges["collection"]
            
            database_names: list[str] = [db_name for db_name in privileges.keys()]
            if not arg_l[0] in database_names:
                return Responses.R4XX.database_not_found(arg_l[0])
            
            collection_names: list[str] = [coll_name for coll_name in privileges[arg_l[0]].keys()]
            if not arg_l[1] in collection_names:
                return Responses.R4XX.collection_not_found(arg_l[1])
    
    return Responses.R2XX.arguments_valid()
 