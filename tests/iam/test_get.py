# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                               test.iam.test_get.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | Parameters |-------------------------------------------------------------------------------------------------------|
credentials: dict[str] = {"username": "iamtest", "password": "123!IamTest", "email": "iamtest@iamtest.com"}
register_base64: str = header_base64_register(credentials['username'], credentials['password'], credentials['email'])
requests.post(f"{root_route}{register_route}", headers={"Register": register_base64})
header: dict[str] = {"Authorization": f"Bearer {token_login(credentials['username'], credentials['password'])}"}
privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
# |--------------------------------------------------------------------------------------------------------------------|

# | Functions |--------------------------------------------------------------------------------------------------------|
def response_assert(hypothetical_response: str, request_obj: requests.models.Response) -> bool:
    return (hypothetical_response == json.loads(request_obj.text)['response'])

def status_code_assert(hypothetical_status_code: int, request_obj: requests.models.Response) -> bool:
    return (hypothetical_status_code == request_obj.status_code)
# |--------------------------------------------------------------------------------------------------------------------|


# | Test Read Database |-----------------------------------------------------------------------------------------------|
def test_read_database() -> None:
    response: requests.models.Response = requests.get(f"{root_route}{database}", headers=header)
    if credentials['username'] in privileges['database']['read']:
        status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Read Collection |---------------------------------------------------------------------------------------------|
def test_read_collection() -> None:
    for database_name in mongo.list_database_names():
        send_json: dict[str] = {"database": database_name}
        response: requests.models.Response = requests.get(f"{root_route}{collection}", headers=header, json=send_json)
        
        if credentials['username'] in privileges['collection']['read']:
            status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Read Documents |----------------------------------------------------------------------------------------------|
def test_read_documents() -> None:
    for database_name in mongo.list_database_names():
        for collection_name in mongo[database_name].list_collection_names():
            send_json: dict[str] = {"database": database_name, "collection": collection_name, "filter": {}}
            response: requests.models.Response = requests.get(f"{root_route}{document}", headers=header, json=send_json)
            
            if database_name in ["config", "admin", "local"]:
                assert response_assert(f"DATABASE [{database_name}] NOT FOUND", response)
                assert status_code_assert(404, response)
            elif credentials["username"] not in privileges[database_name][collection_name]['read']:
                assert response_assert(f"USER [{credentials['username']}] REQUIRE PRIVILEGES", response)
                assert status_code_assert(403, response)
            elif credentials['username'] in privileges[database_name][collection_name]['read']:
                assert status_code_assert(200, response)
# |--------------------------------------------------------------------------------------------------------------------|