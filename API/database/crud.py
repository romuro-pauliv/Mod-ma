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
# +--------------------------------------------------------------------------------------------------------------------+


class ExceptionPass(Exception):
    pass


def parse_json(data: Union[list, dict]) -> json.loads:
    return json.loads(json_util.dumps(data))


def field_validation(input: dict[str, Any]) -> tuple[str, int]:
    denied_fields: list[str] = ["_id", "date", "user"]
    try:
        for field, _ in input.items():
            if field in denied_fields:
                raise ExceptionPass
    except ExceptionPass:
        return "FORBIDDEN", HTTP_403_FORBIDDEN
    return "OK", HTTP_200_OK


def log_create(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple]]:
    def wrapper(*args, **kwargs) -> Callable[[str], tuple]:
        val: Callable[[str], tuple] = func(*args, **kwargs)

        # BSON LOG |---------------------------------------------------------------------------------------------------|
        log: dict = {
            "user": "root",
            "date": ["UTC", datetime.datetime.utcnow()],
            "command": f"CREATE A {func.__name__.upper()}",
            "name": kwargs['name'].lower() if func.__name__ != "document" else val[0][1],
            "code": val[1] 
        }
        # |------------------------------------------------------------------------------------------------------------|

        get_db().LOG.MAINLOG.insert_one(log)    # input in LOG database
        if func.__name__ != "database":
            get_db()[kwargs['database']]['LOG'].insert_one(log)

        return val
    return wrapper


def log_update(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple]]:
    def wrapper(*args, **kwargs) -> Callable[[str], tuple]:
        val: Callable[[str], tuple[str, int]] = func(*args, **kwargs)
        # BSON LOG |---------------------------------------------------------------------------------------------------|
        log: dict = {
            "user": "root",
            "date": ["UTC", datetime.datetime.utcnow()],
            "command": f"UPDATE A {func.__name__.upper()}",
            "name": args[2],
            "code": val[1]
        }
        # |------------------------------------------------------------------------------------------------------------|

        # INPUT LOG |--------------------------------------------------------------------------------------------------|
        get_db()[args[0]].LOG.insert_one(log)
        get_db().LOG.MAINLOG.insert_one(log)
        # |------------------------------------------------------------------------------------------------------------|

        return val
    return wrapper


def log_delete(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple[str, int]]]:
    def wrapper(*args, **kwargs) -> Callable[[str], tuple[str, int]]:
        val: Callable[[str], tuple[str, int]] = func(*args, **kwargs)
        
        #BSON |--------------------------------------------------------------------------------------------------------|
        log: dict = {
            "user": "root",
            "date": ["UTC", datetime.datetime.utcnow()],
            "command": f"DELETE A {func.__name__.upper()}",
            "name": args[2],
            "code": val[1]
        }
        # |------------------------------------------------------------------------------------------------------------|

        # INPUT LOG |--------------------------------------------------------------------------------------------------|
        get_db()[args[0]].LOG.insert_one(log)
        get_db().LOG.MAINLOG.insert_one(log)
        # |------------------------------------------------------------------------------------------------------------|

        return val
    return wrapper

class create(object):
    @log_create
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
    
    @log_create
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

    @log_create
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

        id_str: str = str(ObjectId())

        total_document: dict[str, Any] = {
            "_id": id_str,
            "user": "root",
            "datetime": ['UTC', datetime.datetime.utcnow()]
            }

        total_document.update(document)
        get_db()[database_name][collection_name].insert_one(total_document)

        return ["CREATE", total_document['_id']], HTTP_201_CREATED
    

class read(object):
    def database() -> tuple[list[str], int]:
        return get_db().list_database_names(), HTTP_200_OK
    
    def collection(database: str) -> tuple[Union[list[str], str], int]:
        if database.lower() in get_db().list_database_names():
            return get_db()[database.lower()].list_collection_names(), HTTP_200_OK
        else:
            return 'NOT FOUND', HTTP_404_NOT_FOUND
    
    def all_document(database: str, collection: str) -> tuple[Union[str, list[dict]], int]:
        documents_list: list = []

        if database.lower() not in get_db().list_database_names():
            return 'NOT FOUND', HTTP_404_NOT_FOUND
        
        if collection.lower() not in get_db()[database.lower()].list_collection_names():
            return 'NOT FOUND', HTTP_404_NOT_FOUND

        for document in get_db()[database.lower()][collection.lower()].find({}):
                documents_list.append(document)
        return parse_json(documents_list), HTTP_200_OK


class update(object):
    @log_update
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
    @log_delete
    def document(database: str, collection: str, _id: str) -> tuple[str, int]:
        find_document: dict = parse_json(get_db()[database.lower()][collection.lower()].find({'_id': _id}))
        try:
            if find_document[0]['_id'] == _id:
                get_db()[database.lower()][collection.lower()].delete_one({'_id': _id})
            return 'ACCEPTED', HTTP_202_ACCEPTED
        except IndexError:
            return 'NOT FOUND', HTTP_404_NOT_FOUND 