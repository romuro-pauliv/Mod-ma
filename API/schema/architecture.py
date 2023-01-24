# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         API.schema.architecture.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from pymongo import MongoClient

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from create import *
from schema_data import schema_db
# |--------------------------------------------------------------------------------------------------------------------|

# READ JSON CONTAINING .env PATH |=====================================================================================|
json_path = Path("API/schema/path.json")                # json path
with open(json_path, 'r') as js_file:                   # open json
    json_dt: dict[str] = json.load(js_file)             # load json
    js_file.close()                                     # close json
load_dotenv(dotenv_path=Path(json_dt['dotenv']))        # load .env
# |====================================================================================================================|

# MONGO CLIENT |=======================================================================================================|
def get_db():
    return MongoClient(os.getenv('MONGO_URI'))
# |====================================================================================================================|

# database verification |==============================================================================================|
def create_architecture() -> None:
    db_schema_list: list[str] = []
    for db_name, _ in schema_db.items():
        db_schema_list.append(db_name)
    
    db_list: list[str] = get_db().list_database_names()
    for db in db_schema_list:
        prompt_database("create", db, get_db) if db not in db_list else prompt_database("exists", db)
        
        coll_list: list[str] = get_db()[db].list_collection_names()
        for coll in schema_db[db]:
            prompt_collection("create",coll, db, get_db) if coll not in coll_list else prompt_collection("exists", coll)
        
    user_count: int = get_db().USERS.REGISTER.count_documents({"username": "admin"})
    if user_count == 0:
        prompt_admin_user(mode="create",
                          username="admin",
                          passwd=json_dt['password'],
                          func=get_db)
        prompt_assemble_privileges("admin", get_db)
        prompt_assemble_new_user_privileges(get_db)
    else:
         prompt_admin_user("exists", "admin")
# |====================================================================================================================|