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


class BaseFunctions(object):
    def __init__(self) -> None:
        self.admin_credentials: dict[str] = {
            "username": "admin", "password": "123!Admin"
        }
        self.pamtest_credentials: dict[str] = {
            "username": "pamtest", "password": "123!IamTest", "email": "pamtest@pamtest.com"
        }
        
        self.synthetic_user: dict[str, dict[str]] = {}
        for i in range(1, 7):
            self.synthetic_user[f"user{i}"] = {
                "username": f"pamtest{i}",
                "password": "123!IamTest",
                "email": f"pam{i}test@pamtest.com"
            }
        
    class Register:
        @staticmethod
        def register_user(credentials: dict[str]) -> requests.models.Response:
            crypto_credentials: str = header_base64_register(
                credentials["username"], credentials["password"], credentials["email"]
            )
            header: dict[str] = {
                "Register": crypto_credentials
            }
        
            return requests.post(f"{root_route}{register_route}", headers=header)
    
        @staticmethod
        def delete_user(credentials: dict[str]) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
        
            crypto_credentials: str = header_base64_register(
                credentials["username"], credentials["password"], credentials["email"]
            )
            header: dict[str] = {
                "Register": crypto_credentials,
                "Authorization": f"Bearer {token}"
            }
        
            return requests.delete(f"{root_route}{register_route}", headers=header)
    
    class Privileges:
        @staticmethod
        def verify_in_standard_paper(username: str) -> bool:
            unusable_fields: list[str] = ["_id", "command", "datetime"]
            
            standard_paper: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "standard privileges"})
            privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
            
            for df in unusable_fields:
                del privileges[df]
                del standard_paper[df]
            
            standard_paper_keys: list[str] = [i for i in standard_paper.keys()]
            
            for sp_keys in standard_paper_keys:
                if isinstance(standard_paper[sp_keys], list):
                    methods: list[str] = standard_paper[sp_keys]
                    
                    for method_ in methods:
                        if not username in privileges[sp_keys][method_]:
                            return False
                
                if isinstance(standard_paper[sp_keys], dict):
                    collection_keys_list: list[str] = [coll for coll in standard_paper[sp_keys].keys()]
                    
                    for coll_keys in collection_keys_list:
                        methods: list[str] = standard_paper[sp_keys][coll_keys]
                        
                        for method_ in methods:
                            if not username in privileges[sp_keys][coll_keys][method_]:
                                return False
            
            return True
        
        def vefiry_privileges(username: str, path: list[str]) -> bool:
            privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
            if len(path) == 2:
                if username in privileges[path[0]][path[1]]:
                    return True
            if len(path) == 3:
                if username in privileges[path[0]][path[1]][path[2]]:
                    return True
            
            return False
        
        def get_privileges_list(path: list[str]) -> list[str]:
            privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
            if len(path) == 2:
                return privileges[path[0]][path[1]]
            else:
                return privileges[path[0]][path[1]][path[2]]
        
        def add_or_remove_privileges(
            assignor: dict[str], username: str, method: str, command: str, path: list[str]) -> requests.models.Response:
            token: str = token_login(assignor['username'], assignor['password'])
            header: dict[str] = {"Authorization": f"Basic {token}"}
            
            send_json: dict[str] = {
                "user": username,
                "command": command,
                "method": method,
                "arguments": path
            }
            
            return requests.put(f"{root_route}{iam_route}", headers=header, json=send_json)
        
        
    class Database:
        @staticmethod
        def create(credentials: dict[str], database_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name}
            
            return requests.post(f"{root_route}{database}", headers=header, json=send_json)
        
        def delete(credentials: dict[str], database_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name}
            
            return requests.delete(f"{root_route}{database}", headers=header, json=send_json)


# |====================================================================================================================|
# | TESTS |============================================================================================================|
# |====================================================================================================================|
Base = BaseFunctions()

# | REGISTER USERS |---------------------------------------------------------------------------------------------------|
def test_register_pamtest_user() -> None:
    response: requests.models.Response = Base.Register.register_user(Base.pamtest_credentials)
    
    assert json.loads(response.text)["response"] == "SUCCESSFULLY REGISTERED"
    assert response.status_code == 201


def test_register_synthetic_users() -> None:
    key_list_user: list[str] = [key_user for key_user in Base.synthetic_user.keys()]
    
    for user in key_list_user:
        response: requests.models.Response = Base.Register.register_user(
            Base.synthetic_user[user]
        )
        
        assert json.loads(response.text)["response"] == "SUCCESSFULLY REGISTERED"
        assert response.status_code == 201
# |--------------------------------------------------------------------------------------------------------------------|

# | PRIVILEGES SCHEMA VERIFICATION |-----------------------------------------------------------------------------------|
def test_user_in_standard_privileges() -> None:
    credentials_keys_list: list[str] = [i for i in Base.synthetic_user.keys()]
    
    username_list: list[str] = [Base.synthetic_user[user]["username"] for user in credentials_keys_list]
    username_list.append(Base.pamtest_credentials["username"])
    
    for username in username_list:
        assert True == Base.Privileges.verify_in_standard_paper(username)
# |--------------------------------------------------------------------------------------------------------------------|

# | DATABASE CREATE |--------------------------------------------------------------------------------------------------|
def test_database_create() -> None:
    database_name: str = "testing123321123321"
    
    # | Create without privileges
    response: requests.models.Response = Base.Database.create(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add privileges
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "append", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Create with privileges
    response: requests.models.Response = Base.Database.create(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # | Verify privileges
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["database", "create"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["database", "create"])
    
    # | Remove Privileges
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "remove", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "create"])
        
    # | Delete database
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|


# | DELETE USERS |-----------------------------------------------------------------------------------------------------|
def test_delete_pamtest_user() -> None:
    response: requests.models.Response = Base.Register.delete_user(Base.pamtest_credentials)
    
    assert json.loads(response.text)["response"] == "VALIDATED CREDENTIALS - YOUR ACCOUNT WILL BE DELETED"
    assert response.status_code == 202


def test_delete_synthetic_users() -> None:
    key_list_user: list[str] = [key_user for key_user in Base.synthetic_user.keys()]
    
    for user in key_list_user:
        response: requests.models.Response = Base.Register.delete_user(
            Base.synthetic_user[user]
        )
        
        assert json.loads(response.text)["response"] == "VALIDATED CREDENTIALS - YOUR ACCOUNT WILL BE DELETED"
        assert response.status_code == 202
# |--------------------------------------------------------------------------------------------------------------------|