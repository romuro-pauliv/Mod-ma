# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                         API.iam.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from .db import get_db
from .status import *
# |--------------------------------------------------------------------------------------------------------------------|

class Privileges(object):
    def __init__(self, PAM: str) -> None:
        self.pam = PAM
        self.mongo = get_db
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
    
    def get_keys(self, data: dict[str]) -> list[str]:
        return [i for i in data.keys()]
    
    def update(self) -> None:
        # GET PRIVILEGES JSON |========================================================================================|
        for dt in self.mongo().USERS.PRIVILEGES.find({"command": "privileges"}):
            real_privileges: dict = dt
        # |============================================================================================================|

        mongo_db_list: list[str] = self.mongo().list_database_names()

        # GET NEW DB |=================================================================================================|
        # REGISTERED DB |----------------------------------------------------------------------------------------------|
        registered_db: list[str] = self.get_keys(real_privileges)
        # |------------------------------------------------------------------------------------------------------------|
        
        for db in mongo_db_list:                                          # Iteration of the list from the existing db
            if db not in ["admin", "local"]:                              # Does not perform any acition for the dbs
                
                # UPDATE DATABASE ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if db not in registered_db:                               # Compares registered db with existing ones
                    real_privileges[db]: dict[str, dict] = {}             # Register the new db
                # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                    
                for coll in self.mongo()[db].list_collection_names():     # Iteration of the list from the existing coll
                        
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
            # UPDATE DATABSE +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            if db not in mongo_db_list:                                      # Compares real db with registered
                del real_privileges[db]                                      # Register the delete db
            # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            
            if db in mongo_db_list:
                registered_coll: list[str] = self.get_keys(real_privileges[db])
                for coll in registered_coll:
                    if coll not in self.mongo()[db].list_collection_names():   # Compares real coll with registered
                        del real_privileges[db][coll]                        # Register the delete coll
        # |============================================================================================================|

        # DELETE OLDERS PRIVILEGES |===================================================================================|
        self.mongo().USERS.PRIVILEGES.delete_one({"command": "privileges"})
        # |============================================================================================================|

        # Insert in database |=========================================================================================|
        del real_privileges['_id']
        self.mongo().USERS.PRIVILEGES.insert_one(real_privileges)
    

