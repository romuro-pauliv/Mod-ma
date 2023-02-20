# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                          API.db.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *

from API.secure.token.IPT_token import IPToken

from API.json.responses.database import create_status as database_create_status
from API.json.responses.database import delete_status as database_delete_status

from API.json.responses.collection import create_status as collection_create_status
from API.json.responses.collection import read_status as collection_read_status
from API.json.responses.collection import delete_status as collection_delete_status

from API.json.responses.document import create_status as document_create_status
from API.json.responses.document import read_status as document_read_status
from API.json.responses.document import update_status as document_update_status
from API.json.responses.document import delete_status as document_delete_status

from API.log.model.logs import Create as logCreate
from API.log.model.logs import Update as logUpdate
from API.log.model.logs import Delete as logDelete

from flask import current_app, g, request
from pymongo import MongoClient
from typing import Union, Any

from bson.objectid import ObjectId
from bson import json_util

import datetime
import json
# |--------------------------------------------------------------------------------------------------------------------|

# DATABASE CLIENT |====================================================================================================|
def get_db() -> MongoClient:
    if 'db' not in g:
        g.db = MongoClient(current_app.config['MONGO_URI'])
    return g.db
# |====================================================================================================================|


def parse_json(data: list | dict) -> dict:
    """
    Convert API receive json to dict type for easily handle
    Args: data (list | dict): Unformated json
    Returns: return: dict data 
    """
    return json.loads(json_util.dumps(data))


class create(object):
    def __init__(self) -> None:
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))

    def database(self, database: str) -> tuple[str, int]:
        database: str = database.lower()
        forbidden_database_names: list[str] = [
            "command", "datetime", "database", "collection", "documents", "admin", "local"
        ]
        
        # Forbidden names |--------------------------------------------------------------------------------------------|
        if database in forbidden_database_names:
            return database_create_status.Reponses.R4XX.name_not_allowed(database)
        # |------------------------------------------------------------------------------------------------------------|

        # database search |--------------------------------------------------------------------------------------------|
        if database in get_db().list_database_names():
            return database_create_status.Reponses.R4XX.name_in_use(database)
        # |------------------------------------------------------------------------------------------------------------|

        # Create database |--------------------------------------------------------------------------------------------|
        logCreate.Database.log(database, self.username)
        # |------------------------------------------------------------------------------------------------------------|
        return database_create_status.Reponses.R2XX.create(database)
    
    def collection(self, database: str, collection: str) -> tuple[str, int]:
        database: str = database.lower()              # lowercase database
        collection: str = collection.lower()          # lowercase collection

        # database and collection search |-----------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return collection_create_status.Responses.R4XX.database_not_found(database)
        
        if collection in get_db()[database].list_collection_names():
            return collection_create_status.Responses.R4XX.collection_name_in_use(collection)
        # |------------------------------------------------------------------------------------------------------------|

        # Create collection |------------------------------------------------------------------------------------------|
        logCreate.Collection.log(database, collection, self.username)
        # |------------------------------------------------------------------------------------------------------------|

        return collection_create_status.Responses.R2XX.collection_created(collection)
    
    def document(self, database: str, collection: str, document: str) -> tuple[str, int]:
        database: str = database.lower()       # lowercase database
        collection: str = collection.lower()   # lowercase collection

        # database and collection search |-----------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return document_create_status.Responses.R4XX.database_not_found(database)
        
        if collection not in get_db()[database].list_collection_names():
            return document_create_status.Responses.R4XX.collection_not_found(collection)
        # |------------------------------------------------------------------------------------------------------------|

        # Assemble document |------------------------------------------------------------------------------------------|
        id_str: str = str(ObjectId())

        total_document: dict[str, str | list] = {
            "_id": id_str,
            "user": self.username,
            "datetime": ['UTC', datetime.datetime.utcnow()],
        }

        total_document.update(document)
        # |------------------------------------------------------------------------------------------------------------|

        # Create document |--------------------------------------------------------------------------------------------|
        get_db()[database][collection].insert_one(total_document)
        # |------------------------------------------------------------------------------------------------------------|

        return document_create_status.Responses.R2XX.create_document(id_str)


class read(object):
    def __init__(self) -> None:
        self.usename: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    
    def database(self) -> tuple[list[str], int]:
        return get_db().list_database_names(), HTTP_200_OK
    
    def collection(self, database: str) -> tuple[list[str] | str, int]:
        if database in get_db().list_database_names():
            return get_db()[database].list_collection_names(), HTTP_200_OK
        else:
            return collection_read_status.Responses.R4XX.database_not_found(database)
    
    def document(self, database: str, collection: str, filter: dict[str]) -> tuple[dict[str, Any], int]:

        # Verify if the database and collection exists |---------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return document_read_status.Responses.R4XX.database_not_found(database)
        
        if collection not in get_db()[database].list_collection_names():
            return document_read_status.Responses.R4XX.collection_not_found(collection)
        # |------------------------------------------------------------------------------------------------------------|

        document_list: list[dict[str, Any]] = []
        for document in get_db()[database][collection].find(filter):
            document_list.append(document)
        
        return parse_json(document_list), HTTP_200_OK


class update(object):
    def __init__(self) -> None:
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    
    def document(self, database: str, collection: str, _id: str, new_values: dict[str, Any]) -> tuple[str, int]:
        database: str = database.lower()
        collection: str = collection.lower()
        
        # search database and collection |-----------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return document_update_status.Responses.R4XX.database_not_found(database)
        
        if collection not in get_db()[database].list_collection_names():
            return document_update_status.Responses.R4XX.collection_not_found(collection)
        # |------------------------------------------------------------------------------------------------------------|
        
        # Find document |----------------------------------------------------------------------------------------------|
        real_document: dict[str, Any] = parse_json(get_db()[database][collection].find({"_id": _id}))
        # |------------------------------------------------------------------------------------------------------------|
        
        try:
            # The method serves to filter only the document that not contain ObjectId(). Case the user input the _id
            # refer to ObjectId() (ex.: LOG documents), a exception is called. 
            if real_document[0]["_id"] == _id:
                # Update |-------------------------------------------------------------------------------------------|
                get_db()[database][collection].update_one({"_id": _id}, {"$set": new_values})
                logUpdate.Document.log(database, collection, self.username, _id)
                # |--------------------------------------------------------------------------------------------------|
                return document_update_status.Responses.R2XX.document_updated(_id)
        except IndexError:
            return document_update_status.Responses.R4XX.document_not_found(_id)


class delete(object):
    def __init__(self) -> None:
        self.username: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    
    def delete_database_privileges(self, database: str) -> None:
        get_db().USERS.PRIVILEGES.update_one({"command": "privileges"}, {"$unset": {database: ""}})

    def delete_collection_privileges(self, database: str, collection: str) -> None:
        get_db().USERS.PRIVILEGES.update_one({"command": "privileges"}, {"$unset": {f"{database}.{collection}": ""}})
        
    def database(self, database: str) -> tuple[str, int]:
        database: str = database.lower()
        # | Search database |------------------------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return database_delete_status.Responses.R4XX.not_found(database)
        # | Delete |---------------------------------------------------------------------------------------------------|
        get_db().drop_database(database)
        self.delete_database_privileges(database)
        logDelete.Database.log(database, self.username)
        # |------------------------------------------------------------------------------------------------------------|
        return database_delete_status.Responses.R2XX.delete_database(database)
    
    def collection(self, database: str, collection: str) -> tuple[str, int]:
        database: str = database.lower()
        collection: str = collection.lower()
        
        # | Search database and collection |---------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return collection_delete_status.Responses.R4XX.database_not_found(database)
        
        if collection not in get_db()[database.lower()].list_collection_names():
            return collection_delete_status.Responses.R4XX.collection_not_found(collection)
        # |------------------------------------------------------------------------------------------------------------|
        
        # | Delete |---------------------------------------------------------------------------------------------------|
        get_db()[database].drop_collection(collection)
        self.delete_collection_privileges(database, collection)
        logDelete.Collection.log(database, collection, self.username)
        # |------------------------------------------------------------------------------------------------------------|
        
        return collection_delete_status.Responses.R2XX.collection_deleted(collection)
    
    def document(self, database: str, collection: str, _id: str) -> tuple[str, int]:
        database: str = database.lower()
        collection: str = collection.lower()
        
        # | Search database and collection |---------------------------------------------------------------------------|
        if database not in get_db().list_database_names():
            return document_delete_status.Responses.R4XX.database_not_found(database)
        
        if collection.lower() not in get_db()[database.lower()].list_collection_names():
            return document_delete_status.Responses.R4XX.collection_not_found(collection)
        # |------------------------------------------------------------------------------------------------------------|
        
        # Find document |----------------------------------------------------------------------------------------------|
        real_document: dict[str, Any] = parse_json(get_db()[database.lower()][collection.lower()].find({"_id": _id}))
        # |------------------------------------------------------------------------------------------------------------|
        try:
            # The method serves to filter only the document that not contain ObjectId(). Case the user input the _id
            # refer to ObjectId() (ex.: LOG documents), a exception is called. 
            if real_document[0]["_id"] == _id:
                # | Delete |-------------------------------------------------------------------------------------------|
                get_db()[database][collection].delete_one({"_id": _id})
                logDelete.Document.log(database, collection, _id, self.username)
                # |----------------------------------------------------------------------------------------------------|    
                return document_delete_status.Responses.R2XX.document_deleted(_id)
        except IndexError:
            return document_delete_status.Responses.R4XX.document_not_found(_id)