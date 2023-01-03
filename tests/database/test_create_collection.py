# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                 test.database.create_collection.py |
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


def test_create_database() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll"}

    # + request +
    rtn = requests.post(f"{root_route}{create_database_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201
# |====================================================================================================================|


# |====================================================================================================================|
# | CREATE COLLECTION |================================================================================================|
# |====================================================================================================================|
def test_create_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll", "collection": "test-create-collection"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "CREATE"
    assert rtn.status_code == 201


# |====================================================================================================================|
# | CREATE COLLECTION IN USE |=========================================================================================|
# |====================================================================================================================|
def test_create_collection_in_use() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll", "collection": "test-create-collection"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "FORBIDDEN - COLLECTION NAME IN USE"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | CREATE COLLECTION WITHOUT DATABASE EXISTS |========================================================================|
# |====================================================================================================================|
def test_create_collection_without_database_exists() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll___", "collection": "test-create-collection"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "FORBIDDEN - DATABASE NOT EXISTS"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | CREATE_COLLECTION_WITH_NAME_DATABASE_LESS_THAN_4_CHARACTERS |======================================================|
# |====================================================================================================================|
def test_create_collection_with_name_database_less_than_4_chracters() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "tes", "collection": "test-create-collection"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CREATE_COLLECTION_WITH_NAME_COLLECTION_LESS_THAN_4_CHARACTERS |====================================================|
# |====================================================================================================================|
def test_create_collection_with_name_database_less_than_4_chracters() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll", "collection": "tes"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "THE INFORMED NAME MUST BE MORE THAN 4 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CREATE_COLLECTION_WITH_EMPTY_JSON |================================================================================|
# |====================================================================================================================|
def test_create_collection_with_empty_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CREATE_COLLECTION_WITHOUT_JSON |===================================================================================|
# |====================================================================================================================|
def test_create_collection_without_json() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header)

    # + tests +
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CREATE_COLLECTION_WITHOUT_NECESSARY_FIELD_COLLECTION |=============================================================|
# |====================================================================================================================|
def test_create_collection_without_necessary_field_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[None] = {"database": "test_coll"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CREATE_COLLECTION_WITHOUT_NECESSARY_FIELD_DATABASE |===============================================================|
# |====================================================================================================================|
def test_create_collection_without_necessary_field_collection() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[None] = {"collection": "testing"}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "BAD REQUEST - KEY ERROR"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | CHARACTER_NOT_ALLOWED|=============================================================================================|
# |====================================================================================================================|
def test_create_collection_with_characters_not_allowed() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ \t\n\r\x0b\x0c":
        # + json +
        json_body: dict[None] = {"database": "test_coll", "collection": str("test" + _char)}

        # + request +
        rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

        # + tests +
        assert rtn.text == str("CHARACTER [" + _char + "] NOT ALLOWED")
        assert rtn.status_code == 400


# |====================================================================================================================|
# | NO STRING IN COLLECTION NAME |=====================================================================================|
# |====================================================================================================================|
def test_no_string_in_collection_name() -> None:
    token: str = token_return("admin", "123!Admin")
    # + header +
    header: dict[str] = {"Authorization": f"Token {token}"}

    # + json +
    json_body: dict[str] = {"database": "test_coll", "collection": ["testing", 123123, "hello"]}

    # + request +
    rtn = requests.post(f"{root_route}{create_collection_route}", headers=header, json=json_body)

    # + tests +
    assert rtn.text == "ONLY STRING ARE ALLOWED"
    assert rtn.status_code == 400