# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.database.test_post.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Set data |---------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "admin", "password": "123!Admin"}
header: dict[str] = {"Authorization": f"Bearer {token_return(credentials['username'], credentials['password'])}"}
create_database: str = "testing"
# |--------------------------------------------------------------------------------------------------------------------|

# | function |---------------------------------------------------------------------------------------------------------|
def post_function(json_body: dict[str, Any]) -> requests.models.Response:
    return requests.post(f"{root_route}{database}", headers=header, json=json_body)

def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)["response"])

def status_code_assert(hypothetical_status_code: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test create database |---------------------------------------------------------------------------------------------|
"""
The test below are about the real create database
"""

def test_create_database() -> None:
    database_name: str = create_database
    response: requests.models.Response = post_function({"database": database_name})
    assert response_assert(f"[{database_name}] CREATED", response)
    assert status_code_assert(201, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test create database in use or forbidden |-------------------------------------------------------------------------|
"""
The tests below are about try create exists database
"""

def test_create_database_in_use() -> None:
    database_name: str = create_database
    response: requests.models.Response = post_function({"database": database_name})
    assert response_assert(f"FORBIDDEN - NAME [{database_name}] IN USE", response)
    assert status_code_assert(403, response)


def test_create_forbidden_database() -> None:
    database_name_list: list[str] = ["command", "datetime", "database", "collection", "documents", "admin", "local"]
    for database_name in database_name_list:
        response: requests.models.Response = post_function({"database": database_name})
        assert response_assert(f"FORBIDDEN - NAME [{database_name}] NOT ALLOWED", response)
        assert status_code_assert(403, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test database name syntax |----------------------------------------------------------------------------------------|
"""
The tests below are about database name syntax
"""

def test_database_name_less_than_4_characters() -> None:
    database_name_list: list[str] = ["", "t", "te", "tes"]
    for database_name in database_name_list:
        response: requests.models.Response = post_function({"database": database_name})
        assert response_assert(f"THE INFORMED NAME [{database_name}] MUST BE MORE THAN [4] CHARACTERS", response)
        assert status_code_assert(400, response)


def test_database_name_with_forbidden_characters() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        database_name: str = f"test{_char}ing"
        
        response: requests.models.Response = post_function({"database": database_name})
        assert response_assert(f"CHARACTER [{_char}] IN [{database_name}] NOT ALLOWED", response)
        assert status_code_assert(400, response)
# |--------------------------------------------------------------------------------------------------------------------|


# | Reset |------------------------------------------------------------------------------------------------------------|
"""
The function below not are about a test. The function reset the privileges merged in privileges paper and 
delete database used in above tests
"""

def test_reset() -> None:
    privileges_query: dict[str] = {"command": "privileges"}
    
    mongo.drop_database(create_database)
    privileges: dict[str, list[str] | dict[str]] = mongo.USERS.PRIVILEGES.find_one(privileges_query)
    del privileges['_id']
    del privileges[create_database]
    
    mongo.USERS.PRIVILEGES.delete_one(privileges_query)
    mongo.USERS.PRIVILEGES.insert_one(privileges)
    
    assert isinstance(privileges, dict)