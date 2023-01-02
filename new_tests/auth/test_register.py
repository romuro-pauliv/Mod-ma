# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         test.auth.test_register.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
import os
import json
import base64
import requests
from config import *
# |--------------------------------------------------------------------------------------------------------------------|


# INTIAL CONFIG TO TEST |==============================================================================================|
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
    
    for document in usertest_user:
        try:
            if document['username'] == "user_test":
                assert document['username'] == "user_test"
                mongo.USERS.REGISTER.delete_one({"username":"user_test"})
        except KeyError:
            pass
# |====================================================================================================================|


# |====================================================================================================================|
# | REAL REGISTER |====================================================================================================|
# |====================================================================================================================|
def test_real_register() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("user_test", "123!Admin", "usertest@usertest.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "CREATED"
    assert rtn.status_code == 201

    # +====================+
    # + LOGIN CONFIRMATION +
    # +====================+

    # + header +
    header: dict[str] = {"Authorization": header_base64_login("user_test", "123!Admin")}

    # + request +
    rtn = requests.post(f"{root_route}{login_route}", headers=header)

    # + tests +
    assert json.loads(rtn.text)['token']
    assert json.loads(rtn.text)['token expiration time [UTC]']
    assert rtn.status_code == 202


# |====================================================================================================================|
# | CHARACTER VALIDATION USERNAME |====================================================================================|
# |====================================================================================================================|
def test_character_username_validation_register() -> None:
    for _char in "!\"#$%&'()*+,./:;<=>?@[\]^`{|}~ ":
        # + header +
        header: dict[str] = {"Register": header_base64_register(str("user" + _char), "123!Admin", "test123@test.com")}

        # + request +
        rtn = requests.post(f"{root_route}{register_route}", headers=header)

        # + tests +
        assert rtn.text == str("CHARACTER [" + _char + "] NOT ALLOWED")
        assert rtn.status_code == 400


# |====================================================================================================================|
# | USERNAME LESS THAN 4 CHARACTERS |==================================================================================|
# |====================================================================================================================|
def test_username_less_than_4_character_resgister() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("use", "123!Admin", "test123test@test.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "YOUR USERNAME MUST BE MORE THAN 4 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | PASSWORD LESS THAN 8 CHARACTERS |==================================================================================|
# |====================================================================================================================|
def test_password_less_than_8_characters_register() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("user", "1234", "test12341@test.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + test +
    assert rtn.text == "YOUR PASSWORD MUST BE MORE THAN 8 CHARACTERS"
    assert rtn.status_code == 400


# |====================================================================================================================|
# | ASCII VALIDATION |=================================================================================================|
# |====================================================================================================================|
def test_password_validation_ascii_register() -> None:
    type_char: list[str] = ["lowercase", "uppercase", "digits", "punctuation"]
    password_list: list[str] = ["123!ADMIN", "123!admin", "!adminADMIN", "123Admin"]

    for n, passwd in enumerate(password_list):
        # + header +
        header: dict[str] = {"Register": header_base64_register("user", passwd, "test99876@test.com")}

        # + request +
        rtn = requests.post(f"{root_route}{register_route}", headers=header)

        # + tests +
        assert rtn.text == str("MISSING 1 " + type_char[n].upper() + " CHARACTER")
        assert rtn.status_code == 400


# |====================================================================================================================|
# | USERNAME IN USE |==================================================================================================|
# |====================================================================================================================|
def test_username_in_user_register() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("user_test", "123!Admin", "test87718123@test.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "EMAIL OR USERNAME IN USE"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | EMAIL IN USE |=====================================================================================================|
# |====================================================================================================================|
def test_email_in_use_register() -> None:
    # + header +
    header: dict[str] = {"Register": header_base64_register("test_test", "123!Admin", "usertest@usertest.com")}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + tests +
    assert rtn.text == "EMAIL OR USERNAME IN USE"
    assert rtn.status_code == 403


# |====================================================================================================================|
# | NO REGISTER HEADER |===============================================================================================|
# |====================================================================================================================|
def test_no_header_register() -> None:
    # + header +
    header: dict[None] = {}

    # + request +
    rtn = requests.post(f"{root_route}{register_route}", headers=header)

    # + test +
    assert rtn.text == "BAD REQUEST - NO DATA"
    assert rtn.status_code == 400