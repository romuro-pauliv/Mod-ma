# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                         API.log.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from .db import get_db
from typing import Union, Any, Callable
import datetime
from flask import request
# |--------------------------------------------------------------------------------------------------------------------|


class LogDB(object):
    def log_create(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple]]:
        def wrapper(*args, **kwargs) -> Callable[[str], tuple]:
            # Execute wrapper function |-------------------------------------------------------------------------------|
            val: Callable[[str], tuple] = func(*args, **kwargs)
            # |--------------------------------------------------------------------------------------------------------|

            # BSON LOG |-----------------------------------------------------------------------------------------------|
            log: dict[str, Any] = {
                "user": "root",
                "date": ["UTC", datetime.datetime.utcnow()],
                "command": f"CREATE A {func.__name__.upper()}",
                "name": kwargs['name'].lower() if func.__name__ != "document" else val[0][1],
                "code": val[1] 
            }
            # |--------------------------------------------------------------------------------------------------------|

            # | INPUT LOG |--------------------------------------------------------------------------------------------|
            get_db().LOG.MAINLOG.insert_one(log)                       # input in LOG in MAINLOG
            if func.__name__ != "database":                            # input in internal log if not create database
                get_db()[kwargs['database']]['LOG'].insert_one(log)
            # |--------------------------------------------------------------------------------------------------------|
            return val
        return wrapper
    
    def log_update(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple]]:
        def wrapper(*args, **kwargs) -> Callable[[str], tuple]:
            # | Execute wrapper function |-----------------------------------------------------------------------------|
            val: Callable[[str], tuple[str, int]] = func(*args, **kwargs)
            # |--------------------------------------------------------------------------------------------------------|
            
            # BSON LOG |-----------------------------------------------------------------------------------------------|
            log: dict[str, Any] = {
                "user": "root",
                "date": ["UTC", datetime.datetime.utcnow()],
                "command": f"UPDATE A {func.__name__.upper()}",
                "name": args[2],
                "code": val[1]
            }
            # |--------------------------------------------------------------------------------------------------------|

            # INPUT LOG |----------------------------------------------------------------------------------------------|
            get_db()[args[0]].LOG.insert_one(log)                    # input in internal LOG
            get_db().LOG.MAINLOG.insert_one(log)                     # input in LOG in MAINLOG
            # |--------------------------------------------------------------------------------------------------------|

            return val
        return wrapper
    
    def log_delete(func: Callable[..., Any]) -> Callable[..., Callable[[str], tuple[str, int]]]:
        def wrapper(*args, **kwargs) -> Callable[[str], tuple[str, int]]:
            # | Execute wrapper function |-----------------------------------------------------------------------------|
            val: Callable[[str], tuple[str, int]] = func(*args, **kwargs)
            # |--------------------------------------------------------------------------------------------------------|
        
            # BSON LOG |-----------------------------------------------------------------------------------------------|
            log: dict = {
                "user": "root",
                "date": ["UTC", datetime.datetime.utcnow()],
                "command": f"DELETE A {func.__name__.upper()}",
                "name": args[2],
                "code": val[1]
            }
            # |--------------------------------------------------------------------------------------------------------|

            # INPUT LOG |----------------------------------------------------------------------------------------------|
            get_db()[args[0]].LOG.insert_one(log)                   # input in internal LOG
            get_db().LOG.MAINLOG.insert_one(log)                    # input in LOG in MAINLOG
            # |--------------------------------------------------------------------------------------------------------|

            return val
        return wrapper


class LogAuth(object):
    def login_route(func: Callable[..., Any]) -> Callable[[None], tuple[str, int]]:
        def wrapper(*args, **kwargs) -> Callable[[None], tuple[str, int]]:
            # | Execute wrapper function |-----------------------------------------------------------------------------|
            val: Callable[[None], tuple[str, int]] = func(*args, **kwargs)
            # |--------------------------------------------------------------------------------------------------------|

            # BSON LOG |-----------------------------------------------------------------------------------------------|
            log: dict[str, Any] = {
                "user": "root",
                "date": ["UTC", datetime.datetime.utcnow()],
                "command": f"{func.__name__}",
                "addr": request.remote_addr,
                "code": val[1]
            }
            # |--------------------------------------------------------------------------------------------------------|

            # INPUT LOG |----------------------------------------------------------------------------------------------|
            get_db().LOG.MAINLOG.insert_one(log)
            get_db().USERS.LOG.insert_one(log)
            # |--------------------------------------------------------------------------------------------------------|
            return val
        return wrapper
