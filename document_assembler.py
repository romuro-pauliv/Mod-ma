from pymongo import MongoClient, cursor
from bson import ObjectId
import datetime


class Privileges(object):
    def __init__(self) -> None:
        self.mongo = MongoClient("")
        self.methods: dict[str, list[str]] = {
            "create": [],
            "read": [],
            "update": [],
            "delete": []
        }
    
    def get_all_users(self) -> list[str]:
        users_object: cursor.Cursor = self.mongo.USERS.REGISTER.find({})
        usernames: list[str] = []
        for users in users_object:
            usernames.append(users['username'])
        return usernames
    

    def assemble_privileges(self) -> None:
        # assemble architecture |======================================================================================|
        privileges: dict[str, dict] = {
            "datetime": datetime.datetime.utcnow(),
            "database": self.methods,
            "collection": self.methods,
            "documents": self.methods,
        }
        # |============================================================================================================|
        for db_name in self.mongo.list_database_names():
            if db_name not in ["admin", "local"]:
                privileges[db_name]: dict[str, dict] = {}

                for coll_name in self.mongo[db_name].list_collection_names():
                    privileges[db_name][coll_name] = self.methods
        # |============================================================================================================|

        # Insert in database |=========================================================================================|
        self.mongo.USERS.PRIVILEGES.insert_one(privileges)
        # |============================================================================================================|
