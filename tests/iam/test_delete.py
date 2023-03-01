# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            test.iam.test_delete.py |
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


# | Test Delete Database |---------------------------------------------------------------------------------------------|
def test_delete_database() -> None:
    for database_name in mongo.list_database_names():
        json_send: dict[str] = {"database": database_name}
        response: requests.models.Response = requests.delete(f'{root_route}{database}', headers=header, json=json_send)
        if credentials['username'] not in privileges['database']['delete']:
            assert json.loads(response.text)["response"] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
            assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|


# | Test Delete Collection |-------------------------------------------------------------------------------------------|
def test_delete_collection() -> None:
    for database_name in mongo.list_database_names():
        for collection_name in mongo[database_name].list_collection_names():
            json_send: dict[str] = {"database": database_name, "collection": collection_name}
            response: requests.models.Response = requests.delete(f"{root_route}{collection}",
                                                                 headers=header, json=json_send)
            if credentials['username'] not in privileges['collection']['delete']:
                assert json.loads(response.text)['response'] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
                assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|


# | Test delete document |---------------------------------------------------------------------------------------------|
def test_delete_document() -> None:
    for database_name in mongo.list_database_names():
        for collection_name in mongo[database_name].list_collection_names():
            mongo_document: dict[str, Any] = mongo[database_name][collection_name].find_one({})
            try:
                
                id: str = str(mongo_document["_id"])
                if len(id) == 24:
                    send_json: dict[str] = {"database": database_name, "collection": collection_name, "_id": id}
                    response: requests.models.Response = requests.delete(f"{root_route}{document}",
                                                                         headers=header, json=send_json)
                    if credentials['username'] not in privileges[database_name][collection_name]['delete']:
                        assert json.loads(response.text)["response"] == f"USER [{credentials['username']}] REQUIRE PRIVILEGES"
                        assert response.status_code == 403
                    
            except (KeyError, TypeError):
                pass

# |--------------------------------------------------------------------------------------------------------------------|

