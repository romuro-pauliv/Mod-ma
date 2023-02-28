# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                            test.iam.test_update.py |
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

# | Test Update Documents |--------------------------------------------------------------------------------------------|
def test_update_document() -> None:
    username: str = credentials['username']
    for database_name in mongo.list_database_names():
        for collection_name in mongo[database_name].list_collection_names():
            document_mongo: dict[str, Any] = mongo[database_name][collection_name].find_one({})
            try:
                id: str = str(document_mongo["_id"])
                if len(id) == 24:
                    send_json: dict[str] = {"database": database_name, "collection": collection_name, "_id": id,
                                            "update": {"TESTING": "IAM"}}
                    response: requests.models.Response = requests.put(f"{root_route}{document}", headers=header,
                                                                      json=send_json)
                    
                    if credentials['username'] not in privileges[database_name][collection_name]["update"]:
                        assert json.loads(response.text)['response'] == f"USER [{username}] REQUIRE PRIVILEGES"
                        assert response.status_code == 403
                    else:
                        assert json.loads(response.text)['response'] == f"DATABASE [{database_name}] NOT FOUND"
                        assert response.status_code == 404
            except (KeyError, TypeError):
                pass
# |--------------------------------------------------------------------------------------------------------------------|