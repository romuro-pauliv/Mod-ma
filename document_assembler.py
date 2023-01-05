from pymongo import MongoClient, cursor
from bson import ObjectId
import datetime


class Privileges(object):
    def __init__(self, PAM: str) -> None:
        self.mongo = MongoClient("")
        self.methods: dict[str, list[str]] = {
            "create": [PAM],
            "read": [PAM],
            "update": [PAM],
            "delete": [PAM]
        }
        self.config_names: list[str] = [
            "_id", "command", "datetime",
            "database", "collection", "documents",
            "admin", "local"
            ]
    
    def get_all_users(self) -> list[str]:
        users_object: cursor.Cursor = self.mongo.USERS.REGISTER.find({})
        usernames: list[str] = []
        for users in users_object:
            usernames.append(users['username'])
        return usernames
    

    def get_keys(self, data: dict[str]) -> list[str]:
        keys: list[str] = []
        for d in data.keys():
            keys.append(d)
        return keys
    

    def assemble_privileges(self) -> None:
        # assemble architecture |======================================================================================|
        privileges: dict[str, dict] = {
            "command": "privileges",
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
    
    def update(self) -> dict[str]:
        # GET PRIVILEGES JSON |========================================================================================|
        for dt in self.mongo.USERS.PRIVILEGES.find({"command": "privileges"}):
            real_privileges: dict = dt        
        # |============================================================================================================|
        
        # REGISTERED DB |----------------------------------------------------------------------------------------------|
        registered_db: list[str] = self.get_keys(real_privileges)
        # |------------------------------------------------------------------------------------------------------------|
        
        mongo_db_list: list[str] = self.mongo.list_database_names()

        # GET NEW DB |=================================================================================================|
        for db in mongo_db_list:                                          # Iteration of the list from the existing db
            if db not in ["admin", "local"]:                              # Does not perform any acition for the dbs
                
                # UPDATE DATABASE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if db not in registered_db:                               # Compares registered db with existing ones
                    real_privileges[db]: dict[str, dict] = {}             # Register the new db
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    
                for coll in self.mongo[db].list_collection_names():       # Iteration of the list from the existing coll
                        
                    # REGISTERED COLLECTIONS |-------------------------------------------------------------------------|
                    registered_coll: list[str] = self.get_keys(real_privileges[db])
                    # |------------------------------------------------------------------------------------------------|

                    # UPDATE COLLECTION ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    if coll not in registered_coll:                       # Compares registered coll with existing ones
                        real_privileges[db][coll] = self.methods          # Register the new coll
                    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # |============================================================================================================|

        # DELETE NON-EXISTENT DB |=====================================================================================|
        registered_db: list[str] = [elem for elem in self.get_keys(real_privileges) if elem not in self.config_names]

        for db in registered_db:
            if db not in mongo_db_list:
                del real_privileges[db]
            
            if db in mongo_db_list:
                registered_coll: list[str] = self.get_keys(real_privileges[db])
                for coll in registered_coll:
                    if coll not in self.mongo[db].list_collection_names():
                        del real_privileges[db][coll]
        # |============================================================================================================|

        # DELETE OLDERS PRIVILEGES |===================================================================================|
        self.mongo.USERS.PRIVILEGES.delete_one({"command": "privileges"})
        # |============================================================================================================|

        # Insert in database |=========================================================================================|
        del real_privileges['_id']
        self.mongo.USERS.PRIVILEGES.insert_one(real_privileges)
        # |============================================================================================================|


Privileges("admin").update()