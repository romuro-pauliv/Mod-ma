# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                   test.database.create_database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import requests
from config import *
# |--------------------------------------------------------------------------------------------------------------------|

# | INTIAL CONFIG TO TEST |============================================================================================|
def test_pre_test_delete_users_login() -> None:
    admin_user: dict[str] = mongo.USERS.REGISTER.find({"username":"admin"})
    usertest_user: dict[str] = mongo.USERS.REGISTER.find({"username":"user_test"})

    for document in admin_user:
        try:
            if document['username'] == "admin":
                assert document['username'] == "admin"
                mongo.USERS.REGISTER.delete_one({"username":"admin"})
        except KeyError:
            pass


def test_real_register() -> None:
    # + header build +
    header: dict[str] = {"Register": header_base64_register("admin", "123!Admin", "admin@admin.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "CREATED"
    assert rtn.status_code == 201
# |====================================================================================================================|


# |====================================================================================================================|
# | CREATE DATABASE |==================================================================================================|
# |====================================================================================================================|
def test_create_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | CREATE DATABASE IN USE |===========================================================================================|
# |====================================================================================================================|
def test_create_database_in_use() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "FORBIDDEN - DATABASE NAME IN USE"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | DATABASE NAME LESS THAN 4 CHARACTERS |=============================================================================|
# |====================================================================================================================|
def test_database_name_less_than_4_characters() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "tes"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | EMPTY JSON REQUEST |===============================================================================================|
# |====================================================================================================================|
def test_create_database_with_empty_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | NO JSON REQUEST |==================================================================================================|
# |====================================================================================================================|
def test_create_database_without_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header)

    # + tests +
    assert rtn.status_code == 400

# |====================================================================================================================|
# | JSON WITHOUT NECESSARY FIELD |=====================================================================================|
# |====================================================================================================================|
def test_json_without_necessary_field() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"testing field": "testing"}

    # + json +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CHARACTERS NOT ALLOWED |===========================================================================================|
# |====================================================================================================================|
def test_characters_not_allowed() -> None:
    token: str = token_return("admin", "123!Admin")

    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
        # + json +
        json_body: dict[str] = {"database": str("testing" + _char)}

        # + request +
        rtn  = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

        # + tests +
        assert rtn.text == str("CHARACTER [" + _char + "] NOT ALLOWED")
        assert rtn.status_code == 400


# |====================================================================================================================|
# | NO STRING NAME DATABASE |==========================================================================================|
# |====================================================================================================================|
def test_no_string_value_name_database() -> None:
    token: str = token_return("admin", "123!Admin")

    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str, list] = {"database": ["testing", "name", "database"]}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "ONLY STRING ARE ALLOWED"
    assert rtn.status_code == 400

