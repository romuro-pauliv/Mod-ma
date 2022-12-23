# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               API.database.crud.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports +------------------------------------------------------------------------------------------------------------+
from .db import get_db
from .status import *
from typing import Callable, Any, Union
from bson.objectid import ObjectId
from bson import json_util
import datetime
import json
from .log import LogDB
# +--------------------------------------------------------------------------------------------------------------------+


class ExceptionPass(Exception):
    # Exception pass to raise functions
    pass


def parse_json(data: Union[list, dict]) -> json.loads:
    """Convert API receive json to dict type for easily handle.
    Args: data (Union[list, dict]): Unformated json
    Returns: json.loads: Formated dictionary
    """
    return json.loads(json_util.dumps(data))


def field_validation(input: dict[str, Any]) -> tuple[str, int]:
    """
    Validation of sended json. Serves to don't include fields with date, user, and _id.
    Args:
        input (dict[str, Any]): Json to validation.
    Raises: ExceptionPass: Interrupt the search.
    Returns: tuple[str, int]: HTTP code
    """
    denied_fields: list[str] = ["_id", "date", "user"]
    try:
        for field, _ in input.items():
            if field in denied_fields:
                raise ExceptionPass
    except ExceptionPass:
        return "FORBIDDEN", HTTP_403_FORBIDDEN
    return "OK", HTTP_200_OK


class create(object):
    @LogDB.log_create
    @staticmethod
    def database(name: str) -> tuple[str, int]:
        database_name: str = name.lower()            # lowercase database

        # database search |--------------------------------------------------------------------------------------------|
        if database_name in get_db().list_database_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|
        
        # Create database |--------------------------------------------------------------------------------------------|
        get_db()[database_name]["LOG"].insert_one({
            "user": "root",
            "datetime": ["UTC", datetime.datetime.utcnow()],
            "command": f"Hello, I'm {database_name}",
            })
        # |------------------------------------------------------------------------------------------------------------|

        return "CREATE", HTTP_201_CREATED
    
    @LogDB.log_create
    @staticmethod
    def collection(database: str, name: str) -> tuple[str, int]:
        database_name: str = database.lower()        # lowercase database
        collection_name: str = name.lower()          # lowercase collection

        # datbase and collection search |------------------------------------------------------------------------------|
        if database_name not in get_db().list_database_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        
        if collection_name in get_db()[database_name].list_collection_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        # Create collection |------------------------------------------------------------------------------------------|
        get_db()[database_name][collection_name].insert_one({
            "user": "root",
            "datetime": ["UTC", datetime.datetime.utcnow()],
            "command": f"Hello, I'm {collection_name}",
        })
        # |------------------------------------------------------------------------------------------------------------|

        return "CREATE", HTTP_201_CREATED

    @LogDB.log_create
    @staticmethod
    def document(database: str, collection: str, document: dict) -> tuple[Union[list, str], int]:
        database_name: str = database.lower()       # lowercase database
        collection_name: str = collection.lower()   # lowercase collection

        # database and collection search |-----------------------------------------------------------------------------|
        if database_name not in get_db().list_database_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN

        if collection_name not in get_db()[database_name].list_collection_names():
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|

        # fields validation |------------------------------------------------------------------------------------------|
        if field_validation(document)[1] == 403:
            return "FORBIDDEN", HTTP_403_FORBIDDEN
        # |------------------------------------------------------------------------------------------------------------|
        
        # Assemble document |------------------------------------------------------------------------------------------|
        id_str: str = str(ObjectId())

        total_document: dict[str, Any] = {
            "_id": id_str,
            "user": "root",
            "datetime": ['UTC', datetime.datetime.utcnow()]
            }

        total_document.update(document)
        # |------------------------------------------------------------------------------------------------------------|
        
        # Create document |--------------------------------------------------------------------------------------------|
        get_db()[database_name][collection_name].insert_one(total_document)
        # |------------------------------------------------------------------------------------------------------------|

        return ["CREATE", total_document['_id']], HTTP_201_CREATED
    

class read(object):
    def database() -> tuple[list[str], int]:
        return get_db().list_database_names(), HTTP_200_OK
    
    def collection(database: str) -> tuple[Union[list[str], str], int]:
        if database.lower() in get_db().list_database_names():                            # Verify the database exists |
            return get_db()[database.lower()].list_collection_names(), HTTP_200_OK
        else:
            return 'NOT FOUND', HTTP_404_NOT_FOUND
    
    def all_document(database: str, collection: str) -> tuple[Union[str, list[dict]], int]:
        documents_list: list = []

        # Verify if the database and collection exists |---------------------------------------------------------------|
        if database.lower() not in get_db().list_database_names():
            return 'NOT FOUND', HTTP_404_NOT_FOUND
        
        if collection.lower() not in get_db()[database.lower()].list_collection_names():
            return 'NOT FOUND', HTTP_404_NOT_FOUND
        # |------------------------------------------------------------------------------------------------------------|

        for document in get_db()[database.lower()][collection.lower()].find({}):
                documents_list.append(document)
        return parse_json(documents_list), HTTP_200_OK
    
    def search_document_for_field_value(
        database: str, collection: str, field_value: dict[str, Any]) -> tuple[Union[str, list[dict]], int]:
        documents_list: list = []

        # Verify if the database and collection exists |---------------------------------------------------------------|
        if database.lower() not in get_db().list_database_names():
            return "NOT FOUND", HTTP_404_NOT_FOUND
        
        if collection.lower() not in get_db()[database.lower()].list_collection_names():
            return 'NOT FOUND', HTTP_404_NOT_FOUND
        # |------------------------------------------------------------------------------------------------------------|

        for document in get_db()[database.lower()][collection.lower()].find(field_value):
            documents_list.append(document)
        
        if documents_list == []:
            return 'NOT FOUND', HTTP_404_NOT_FOUND
        else:
            return parse_json(documents_list), HTTP_200_OK


class update(object):
    @LogDB.log_update
    @staticmethod
    def document(database: str, collection: str, _id: str, new_values: dict) -> tuple[str, int]:
        # search database and collection |-----------------------------------------------------------------------------|
        if database.lower() not in get_db().list_database_names():
            return "NOT FOUND", HTTP_404_NOT_FOUND
        
        if collection.lower() not in get_db()[database.lower()].list_collection_names():
            return "NOT FOUND", HTTP_404_NOT_FOUND
        # |------------------------------------------------------------------------------------------------------------|

        # Find document and convert to parse_json
        find_document: dict = parse_json(get_db()[database.lower()][collection.lower()].find({'_id': _id}))
        
        try:
            # The method serves to filter only the document that not contain ObjectId(). Case the user input the _id
            # refer to ObjectId() (ex.: LOG documents), a exception is called. 
            if find_document[0]['_id'] == _id:
                if field_validation(new_values)[1] == 200:
                    
                    filter: dict = {"_id": _id}
                    updating: dict = {"$set": new_values}
                    
                    get_db()[database.lower()][collection.lower()].update_one(filter, updating)
                    return "CREATED", HTTP_201_CREATED
                else:
                    return "FORBIDDEN", HTTP_403_FORBIDDEN
        except IndexError:
            return 'NOT FOUND', HTTP_404_NOT_FOUND


class drop(object):
    @LogDB.log_delete
    @staticmethod
    def document(database: str, collection: str, _id: str) -> tuple[str, int]:
        # Find document and convert to parse_json
        find_document: dict = parse_json(get_db()[database.lower()][collection.lower()].find({'_id': _id}))
        
        try:
            if find_document[0]['_id'] == _id:
                get_db()[database.lower()][collection.lower()].delete_one({'_id': _id})
            
            return 'ACCEPTED', HTTP_202_ACCEPTED
        except IndexError:
            return 'NOT FOUND', HTTP_404_NOT_FOUND 