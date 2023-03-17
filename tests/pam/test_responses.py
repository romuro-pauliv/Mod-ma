# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.pam.test_responses.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

# | FUNCTIONS |--------------------------------------------------------------------------------------------------------|
def PAM_function(header: dict[str], send_json: dict[str, str | list[str]]) -> requests.models.Response:
    return requests.put(f"{root_route}{iam_route}", headers=header, json=send_json)
# |--------------------------------------------------------------------------------------------------------------------|

# | Admin Credentials |------------------------------------------------------------------------------------------------|
cred_admin: dict[str] = {"username": "admin", "password": "123!Admin"}
admin_header: dict[str] = {"Authorization": f"Basic {token_login(cred_admin['username'], cred_admin['password'])}"}
# |--------------------------------------------------------------------------------------------------------------------|

# | New user to test pam functionalities |-----------------------------------------------------------------------------|
register_pamtest: dict[str] = {"username": "pamtest", "password": "123!PamTest", "email": "pamtest@pamtest.com"}

def test_pam_register() -> None:
    response: requests.models.Response = requests.post(
        f"{root_route}{register_route}", headers={
            "Register": header_base64_register(
                username=register_pamtest["username"],
                password=register_pamtest["password"],
                email=register_pamtest["email"]
            )
        }
    )
    
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|

# | Json Test |--------------------------------------------------------------------------------------------------------|
def test_no_json() -> None:
    response: requests.models.Response = PAM_function(admin_header, None)    
    assert response.status_code == 400


def test_send_no_json() -> None:
    send_json_list: list[str, list[str], float, int] = ["test", ["test", "mode"], 1.12, 123]
    
    for send_json in send_json_list:
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == "ONLY JSON ARE ALLOWED"
        assert response.status_code == 400


def test_required_fields() -> None:
    send_json_list: list[dict[str]] = [
        {"command": "append", "method": "create", "arguments": "database"},
        {"user": "pamtest", "method": "create", "arguments": "database"},
        {"user": "pamtest", "command": "append", "arguments": "database"},
        {"user": "pamtest", "command": "append", "method": "create"}
    ]
    
    for send_json in send_json_list:
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == "BAD REQUEST - KEY ERROR"
        assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|


# | Test in User Value |-----------------------------------------------------------------------------------------------|
def test_no_str_in_username() -> None:
    user_list: list[list[str], dict[str], float] = [["testing", "mode"], {"testing": "mode"}, 1.12321]
    
    for user in user_list:
        send_json: dict[str, Any] = {"user": user, "command": "append", "method": "create", "arguments": "database"}
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == "ONLY STRING ARE ALLOWED"
        assert response.status_code == 400


def test_forbidden_character_in_username() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\\]^`{|}~ ":
        user: str = f"pam{_char}test"
        
        send_json: dict[str, Any] = {"user": user, "command": "append", "method": "create", "arguments": "database"}
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == f"CHARACTER [{_char}] IN [{user}] NOT ALLOWED"
        assert response.status_code == 400


def test_username_not_found() -> None:
    user_list: list[str] = ["pamtest1231231921312931", "testingpam8191273"]
    
    for user in user_list:
        send_json: dict[str] = {"user": user, "command": "append", "method": "create", "arguments": "database"}
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == f"USER [{user}] NOT FOUND"
        assert response.status_code == 404
# |--------------------------------------------------------------------------------------------------------------------|

# | Test in Command Value |--------------------------------------------------------------------------------------------|
def test_no_str_in_command() -> None:
    command_list: list[list[str], dict[str], float] = [["testing", "mode"], {"testing": "mode"}, 1.12312]
    
    for command in command_list:
        send_json: dict[str] = {
            "user": register_pamtest['username'],
            "command": command,
            "method": "create",
            "arguments": "database"
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == "ONLY STRING ARE ALLOWED"
        assert response.status_code == 400


def test_invalid_command() -> None:
    command_list: list[str] = ["removed", "added", "appended", "testing"]
    
    for command in command_list:
        send_json: dict[str] = {
            "user": register_pamtest['username'],
            "command": command,
            "method": "create",
            "arguments": "database"
        }
        
        reponse: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(reponse.text)["response"] == f"INVALID COMMAND - [{command}]"
        assert reponse.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Test in Method Value |---------------------------------------------------------------------------------------------|
def test_no_str_in_method() -> None:
    method_list: list[list[str], dict[str], float] = [["testing", "mode"], {"testing": "mode"}, 1.123321]
    
    for method_ in method_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": method_,
            "arguments": "database"
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)['response'] == "ONLY STRING ARE ALLOWED"
        assert response.status_code == 400


def test_invalid_method() -> None:
    method_list: list[str] = ["created", "reading", "putting", "deleted"]
    
    for method_ in method_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": method_,
            "arguments": "database"
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == f"INVALID CRUD METHOD - [{method_}]"
        assert response.status_code == 400
# |--------------------------------------------------------------------------------------------------------------------|

# | Test Arguments Value |---------------------------------------------------------------------------------------------|
def test_no_list_in_arguments() -> None:
    argument_value_list: list[int, str, float, dict[str]] = [12, "database", 1.12, {"testing": "mothod"}]
    
    for arguments in argument_value_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": "create",
            "arguments": arguments
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == f"INVALID OBJECT TYPE IN [ARGUMENTS] FIELD"
        assert response.status_code == 400


def test_no_str_or_list_in_arguments_items() -> None:
    arguments_item_list: list[int, float, dict] = [1, 1.12, {"testing": "mode"}]
    
    for arguments in arguments_item_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": "create",
            "arguments": [arguments]
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == \
            f"INVALID ITEM TYPE IN ARGUMENTS - ONLY STRING OR LIST - [{str(arguments)}]"
        assert response.status_code == 400


def test_invalid_str_path_arguments() -> None:
    arguments_path_list: list[str] = ["testing", "mode", "databasea", "colection"]
    
    for arguments in arguments_path_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": "create",
            "arguments": [arguments]
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == f"INVALID PATH [{arguments}]"
        assert response.status_code == 400


def test_invalid_list_len_path_arguments() -> None:
    arguments_path_list: list[list[str]] = [["testing"], ["testing", "mode", "test"], []]
    
    for arguments in arguments_path_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": "create",
            "arguments": [arguments]
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == \
            f"INVALID PATH - THE LIST MUST HAVE ONLY 2 ARGUMENTS [{str(arguments)}]"
        assert response.status_code == 400


def test_invalid_list_item_in_arguments() -> None:
    arguments_path_list: list[list[int, float]] = [[21, "mode"], [{"testing": "mode"}, 1.2321], [[], []]]
    
    for arguments in arguments_path_list:
        send_json: dict[str] = {
            "user": register_pamtest["username"],
            "command": "append",
            "method": "create",
            "arguments": [arguments]
        }
        
        response: requests.models.Response = PAM_function(admin_header, send_json)
        
        assert json.loads(response.text)["response"] == \
            f"INVALID OBJECT TYPE IN LIST - {[str(arguments[0])]} - MUST BE A STRING"
        assert response.status_code == 400


def test_arguments_database_not_found() -> None:
    database_name: str = "databasenotfound123321"
    send_json: dict[str] = {
        "user": register_pamtest["username"],
        "command": "append",
        "method": "create",
        "arguments": [[database_name, "collection"]]
    }
    
    response: requests.models.Response = PAM_function(admin_header, send_json)
    
    assert json.loads(response.text)["response"] == f"DATABASE [{database_name}] NOT FOUND"
    assert response.status_code == 404


def test_arguments_collection_not_found() -> None:
    collection_name: str = "collectionnotfound12321"
    send_json: dict[str] = {
        "user": register_pamtest["username"],
        "command": "append",
        "method": "create",
        "arguments": [["PERSON", collection_name]]
    }
    
    response: requests.models.Response = PAM_function(admin_header, send_json)
    
    assert json.loads(response.text)["response"] == f"COLLECTION [{collection_name}] NOT FOUND"
    assert response.status_code == 404
# |--------------------------------------------------------------------------------------------------------------------|


# | Unauthorized PAM user |--------------------------------------------------------------------------------------------|
def test_unauthorized_pam_user() -> None:
    new_user_header: dict[str] = {
        "Authorization": f"Basic {token_login(register_pamtest['username'], register_pamtest['password'])}"
    }
    
    send_json: dict[str] = {
        "user": "admin",
        "command": "remove",
        "method": "create",
        "arguments": ["database"]
    }
    
    response: requests.models.Response = PAM_function(new_user_header, send_json)
    
    assert json.loads(response.text)["response"] == f"FORBIDDEN - USER [{register_pamtest['username']}] UNAUTHORIZED"
    assert response.status_code == 403
# |--------------------------------------------------------------------------------------------------------------------|


# | RESET USER |-------------------------------------------------------------------------------------------------------|
def test_reset_pamtest() -> None:
    header: dict[str] = {
        "Authorization":f"Basic {token_login(register_pamtest['username'], register_pamtest['password'])}",
        "Register": header_base64_register(
            username=register_pamtest['username'],
            password=register_pamtest['password'],
            email=register_pamtest['email']
        )
    }
    
    response: requests.models.Response = requests.delete(f"{root_route}{register_route}", headers=header)
    assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|