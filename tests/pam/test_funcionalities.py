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
        
        @staticmethod
        def vefiry_privileges(username: str, path: list[str]) -> bool:
            privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
            if len(path) == 2:
                if username in privileges[path[0]][path[1]]:
                    return True
            if len(path) == 3:
                if username in privileges[path[0]][path[1]][path[2]]:
                    return True
            
            return False
        
        @staticmethod
        def get_privileges_list(path: list[str]) -> list[str]:
            privileges: dict[str, list | dict] = mongo.USERS.PRIVILEGES.find_one({"command": "privileges"})
            if len(path) == 2:
                return privileges[path[0]][path[1]]
            else:
                return privileges[path[0]][path[1]][path[2]]
        
        @staticmethod
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
        
        @staticmethod
        def read(credentials: dict[str]) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            return requests.get(f"{root_route}{database}", headers=header)
        
        @staticmethod
        def delete(credentials: dict[str], database_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name}
            
            return requests.delete(f"{root_route}{database}", headers=header, json=send_json)
    
    class Collection:
        @staticmethod
        def create(credentials: dict[str], database_name: str, collection_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name, "collection": collection_name}
            
            return requests.post(f"{root_route}{collection}", headers=header, json=send_json)
        
        @staticmethod
        def read(credentials: dict[str], database_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name}
            
            return requests.get(f"{root_route}{collection}", headers=header, json=send_json)
        
        @staticmethod
        def delete(credentials: dict[str], database_name: str, collection_name: str) -> requests.models.Response:
            token: str = token_login(credentials["username"], credentials["password"])
            header: dict[str] = {"Authorization": f"Bearer {token}"}
            
            send_json: dict[str] = {"database": database_name, "collection": collection_name}
            
            return requests.delete(f"{root_route}{collection}", headers=header, json=send_json)

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
    
    # | Adjust privileges |--------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["database", "create"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "create", "remove", ["database"]
        )
        
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Create without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add privileges to pamtest |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "append", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Add privileges to synthetic users |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        synthetic_user_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "create", "append", ["database"]
        )
        
        assert json.loads(synthetic_user_response.text)["response"] == "UPDATE PRIVILEGES"
        assert synthetic_user_response.status_code == 202
    
    # | Create with privileges |---------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # | Verify privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["database", "create"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["database", "create"])
    
    # | Remove pamtest Privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "remove", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # Verify Privileges |----------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "create"])
    
    # | Create without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove synthetic_user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "create", "remove", ["database"]
        )
        
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # Verify synthetic_user Privileges |-------------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "create"])
    
    # | Delete database |----------------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202


def test_database_read() -> None:
    # Adjust privileges |----------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["database", "read"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "read", "remove", ["database"]
        )
        
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Read without privileges |--------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.read(Base.pamtest_credentials)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add Privileges to pamtest |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "read", "append", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Add Privileges to synthetic users |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "read", "append", ["database"]
        )
        
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Read with privileges |-----------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.read(Base.pamtest_credentials)
    assert isinstance(json.loads(response.text), list) == True
    assert response.status_code == 200
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["database", "read"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["database", "read"])
    
    # | Remove pamtest Privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "read", "remove", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "read"])
    
    # | Read without privileges |--------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.read(Base.pamtest_credentials)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove synthetic_user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "read", "remove", ["database"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Verify synthetic_user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "read"])


def test_database_delete() -> None:
    database_name: str = "pamtesting123321123321"
    
    # | Adjust privileges |--------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["database", "delete"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "remove", ["database"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Create database to tests |-------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # | Delete without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add privileges to pamtest |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "append", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Add privileges to synthetic users |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        synthetic_user_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "delete", "append", ["database"]
        )
        
        assert json.loads(synthetic_user_response.text)["response"] == "UPDATE PRIVILEGES"
        assert synthetic_user_response.status_code == 202
    
    # | Delete with privileges |---------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202
    
    # | Verify privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["database", "delete"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["database", "delete"])
    
    # | Remove pamtest Privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "remove", ["database"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "delete"])
    
    # | Create database to test again |--------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # | Delete without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove synthetic user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "delete", "remove", ["database"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Verify synthetic user privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["database", "delete"])
    
    # | Delete Database |----------------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202
    
# |--------------------------------------------------------------------------------------------------------------------|

# COLLECTION |---------------------------------------------------------------------------------------------------------|
def test_collection_create() -> None:
    database_name: str = "testing12333212321"
    collection_name: str = "testing123321232321"
    
    # | Adjust privileges |--------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["collection", "create"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "create", "remove", ["collection"]
        )
        
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Create Database to tests |-------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # Create collection without privileges |---------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.create(
        Base.pamtest_credentials, database_name, collection_name
    )
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # Add privileges to pamtest \--------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "append", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202

    # | Add privileges to synthetic users |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        synthetic_user_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "create", "append", ["collection"]
        )
        assert json.loads(synthetic_user_response.text)["response"] == "UPDATE PRIVILEGES"
        assert synthetic_user_response.status_code == 202

    # | Create with privileges |---------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.create(
        Base.admin_credentials, database_name, collection_name
    )
    assert json.loads(response.text)["response"] == f"[{collection_name}] CREATED"
    assert response.status_code == 201
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["collection", "create"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["collection", "create"])
    
    # | Remove pamtest Privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "create", "remove", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "create"])
    
    # | Create without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.create(
        Base.pamtest_credentials, database_name, collection_name
    )
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove synthetic user privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "create", "remove", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == 'UPDATE PRIVILEGES'
        assert pam_response.status_code == 202
    
    # | Verify synthetic_user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "create"])
    
    # | Delete Database |----------------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202


def test_collection_read() -> None:
    database_name: str = "testing123321321231"
    
    # Create database to test |----------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    # Adjust privileges |----------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["collection", "read"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "read", "remove", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    
    # | Read without privileges |--------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.read(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add Privileges to pamtest |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "read", "append", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Add privleges to synthetic users |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "read", "append", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Read with Privileges |-----------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.read(Base.pamtest_credentials, database_name)
    assert isinstance(json.loads(response.text), list)
    assert response.status_code == 200
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["collection", "read"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["collection", "read"])
    
    # | Remove pamtest Privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "read", "remove", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "read"])
    
    # | Read without privileges |--------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.read(Base.pamtest_credentials, database_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove Synthetic Users Privileges |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "read", "remove", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Verify synthetic user privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "read"])
    
    # Delete Database |------------------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202


def test_collection_delete() -> None:
    database_name: str = "testing123123123812931"
    collection_name: str = "testing1238312382311"
    
    # | Adjust privileges |--------------------------------------------------------------------------------------------|
    if Base.pamtest_credentials["username"] in Base.Privileges.get_privileges_list(["collection", "delete"]):
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "remove", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Create Database and collection to tests |----------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.create(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] CREATED"
    assert response.status_code == 201
    
    response: requests.models.Response = Base.Collection.create(Base.admin_credentials, database_name, collection_name)
    assert json.loads(response.text)["response"] == f"[{collection_name}] CREATED"
    assert response.status_code == 201
    
    # | Delete without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.delete(Base.pamtest_credentials, database_name, collection_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Add privileges to pamtest |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "append", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Add privileges to synthetic users |----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        synthetic_user_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "delete", "append", ["collection"]
        )
        assert json.loads(synthetic_user_response.text)["response"] == "UPDATE PRIVILEGES"
        assert synthetic_user_response.status_code == 202
    
    # | Delete with Privileges |---------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.delete(Base.pamtest_credentials, database_name, collection_name)
    assert json.loads(response.text)["response"] == f"[{collection_name}] COLLECTION DELETED"
    assert response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    assert Base.Privileges.vefiry_privileges(Base.pamtest_credentials["username"], ["collection", "delete"]) == True
    before_user_privileges: list[str] = Base.Privileges.get_privileges_list(["collection", "delete"])
    
    # | Remove pamtest privileges |------------------------------------------------------------------------------------|
    pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
        Base.admin_credentials, Base.pamtest_credentials["username"], "delete", "remove", ["collection"]
    )
    assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
    assert pam_response.status_code == 202
    
    # | Verify Privileges |--------------------------------------------------------------------------------------------|
    before_user_privileges.remove(Base.pamtest_credentials["username"])
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "delete"])
    
    # | Create collection to test again |------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.create(Base.admin_credentials, database_name, collection_name)
    assert json.loads(response.text)["response"] == f"[{collection_name}] CREATED"
    assert response.status_code == 201
    
    # | Delete without privileges |------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Collection.delete(Base.pamtest_credentials, database_name, collection_name)
    assert json.loads(response.text)["response"] == f"USER [{Base.pamtest_credentials['username']}] REQUIRE PRIVILEGES"
    assert response.status_code == 403
    
    # | Remove synthetic user Privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        pam_response: requests.models.Response = Base.Privileges.add_or_remove_privileges(
            Base.admin_credentials, Base.synthetic_user[user]["username"], "delete", "remove", ["collection"]
        )
        assert json.loads(pam_response.text)["response"] == "UPDATE PRIVILEGES"
        assert pam_response.status_code == 202
    
    # | Verify synthetic user privileges |-----------------------------------------------------------------------------|
    for user in [key_user for key_user in Base.synthetic_user.keys()]:
        before_user_privileges.remove(Base.synthetic_user[user]["username"])
    
    assert before_user_privileges == Base.Privileges.get_privileges_list(["collection", "delete"])
    
    # | Delete Database |----------------------------------------------------------------------------------------------|
    response: requests.models.Response = Base.Database.delete(Base.admin_credentials, database_name)
    assert json.loads(response.text)["response"] == f"[{database_name}] DATABASE DELETED"
    assert response.status_code == 202
            
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