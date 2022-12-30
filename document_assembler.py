from pymongo import MongoClient
from bson import ObjectId
import datetime

mongo = MongoClient("")

methods: dict[str, bool] = {
    "create": True,
    "read": True,
    "update": True,
    "delete": True
}

# Structure assembler |------------------------------------------------------------------------------------------------|
privileges: dict[str, dict] = {
    "datetime": datetime.datetime.utcnow(),
    "username": "admin",
    "database": methods,
    "collection": methods,
    "documents": methods
}
for db_name in mongo.list_database_names():
    privileges[db_name]: dict[str] = {}

    for coll_name in mongo[db_name].list_collection_names():
        privileges[db_name][coll_name] = methods
# |--------------------------------------------------------------------------------------------------------------------|

mongo.USERS.PRIVILEGES.insert_one(privileges)
        
