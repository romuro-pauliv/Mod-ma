# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.log.create.logs.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from flask import g
import datetime
from pymongo import MongoClient
# |--------------------------------------------------------------------------------------------------------------------|

def get_db() -> MongoClient:
    return g.db

def log_model(database: str, collection: str, username: str, LOG: str | dict[str]) -> None:
    document: dict[str, str | list] = {
        "user": username,
        "datetime": ["UTC", datetime.datetime.utcnow()],
        "log": LOG,
    }
    get_db()[database][collection].insert_one(document)

# | CREATE |-----------------------------------------------------------------------------------------------------------|
class Create(object):
    class Database(object):
        @staticmethod
        def log(database: str, username: str) -> None:
            log_model(database, "LOG", username, f"Hello, I'm {database}")
            log_model("LOG", "MAINLOG", username, {
                "command": "create database",
                "database": database
            })
    
    class Collection(object):
        @staticmethod
        def log(database: str, collection: str, username: str) -> None:
            log_model(database, collection, username, f"Hello, I'm [{collection}] collection in [{database}] database")
            log_model(database, "LOG", username, {
                "command": "create collection",
                "collection": collection
            })
            log_model("LOG", "MAINLOG", username, {
                "command": "create collection",
                "database": database,
                "collection": collection
            })
# |--------------------------------------------------------------------------------------------------------------------|

# | UPDATE |-----------------------------------------------------------------------------------------------------------|
class Update(object):
    class Document(object):
        @staticmethod
        def log(database: str, collection: str, username: str, document_id: str) -> None:
            log_model(database, "LOG", username, {
                "command": "update document",
                "collection": collection,
                "document_id": document_id
            })
            
            log_model("LOG", "MAINLOG", username, {
                "command": "update document",
                "database": database,
                "collection": collection,
                "document_id": document_id
            })
# |--------------------------------------------------------------------------------------------------------------------|

# | DELETE |-----------------------------------------------------------------------------------------------------------|
class Delete(object):
    class Database(object):
        @staticmethod
        def log(database: str, username: str) -> None:
            log_model("LOG", "MAINLOG", username, {
                "command": "delete database",
                "database": database
            })
    
    class Collection(object):
        @staticmethod
        def log(database: str, collection: str, username: str) -> None:
            log_model("LOG", "MAINLOG", username, {
                "command": "delete collection",
                "database": database,
                "collection": collection
            })
            log_model(database, "LOG", username, {
                "command": "delete collection",
                "collection": collection
            })

    class Document(object):
        @staticmethod
        def log(database: str, collection: str, document_id: str, username: str) -> None:
            log_model("LOG", "MAINLOG", username, {
                "command": "delete document",
                "database": database,
                "collection": collection,
                "document_id": document_id
            })
            log_model(database, "LOG", username, {
                "command": "delete document",
                "collection": collection,
                "document_id": document_id
            })
# |--------------------------------------------------------------------------------------------------------------------|