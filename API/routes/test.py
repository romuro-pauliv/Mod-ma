# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.test.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, update
from API.iam import IAM, Privileges

from API.models.route_test import Model
from API.models.routes.tests.decorators import Model as NewModel

from API.secure.token.IPT_token import required_token, IPToken

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint('test', __name__, url_prefix='/tests')
privileges_add = Privileges("admin").Add()

# |====================================================================================================================|
# | TEST TOKEN |=======================================================================================================|
# |====================================================================================================================|
@bp.route('/test-token', methods=['POST'])
@required_token
def test_token() -> tuple[str, int]:
    return 'TEST OK', HTTP_202_ACCEPTED
# |====================================================================================================================|

# |====================================================================================================================|
# | TEST CREATE DATABASE |=============================================================================================|
# |====================================================================================================================|
@bp.route('/test-create-database', methods=['POST'])
@required_token
@NewModel.Create.database
@IAM.check_permission("create", "database")
@privileges_add.database
def test_create_database() -> tuple[str, int]:
    
    # GET USERNAME AND DATABASE NAME |---------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    database_name_json: str = request.json["database"]
    # |----------------------------------------------------------------------------------------------------------------|

    return create(srnm).database(database_name_json)
# |====================================================================================================================|

# |====================================================================================================================|
# | TEST CREATE COLLECTION |===========================================================================================|
# |====================================================================================================================|
@bp.route("/test-create-collection", methods=['POST'])
@required_token
@Model.create_collection
@IAM.check_permission("create", "collection")
@privileges_add.collection
def test_create_collection() -> tuple[str, int]:

    # GET USERNAME AND JSON RESPONSE |---------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    response: dict[str, str] = request.json
    # |----------------------------------------------------------------------------------------------------------------|

    return create(srnm).collection(response['database'], response['collection'])
# |====================================================================================================================|

# |====================================================================================================================|
# | TEST CREATE DOCUMENT |=============================================================================================|
# |====================================================================================================================|
@bp.route("/test-create-document", methods=["POST"])
@required_token
@Model.create_document
@IAM.check_permission("create", "especific")
def test_create_document() -> tuple[str, int]:

    # GET USERNAME AND JSON RESPONSE |---------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    response: dict[str, str | dict] = request.json
    # |----------------------------------------------------------------------------------------------------------------|

    return create(srnm).document(response['database'], response['collection'], response['document'])
# |====================================================================================================================|

# |====================================================================================================================|
# | TEST READ DATABASE |===============================================================================================|
# |====================================================================================================================|
@bp.route("/test-read-database", methods=["GET"])
@required_token
@IAM.check_permission("read", "database")
def test_read_database() -> tuple[list[str], int]:
    # GET USERNAME |---------------------------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    # |----------------------------------------------------------------------------------------------------------------|
    return read(srnm).database()

# |====================================================================================================================|
# | TEST READ COLLECTION |=============================================================================================|
# |====================================================================================================================|
@bp.route("/test-read-collection", methods=["GET"])
@required_token
@Model.read_collection
@IAM.check_permission("read", "collection")
def test_read_collection() -> tuple[list[str] | str, int]:
    # GET USERNAME AND JSON REQUEST |----------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    response: dict[str] = request.json
    # |----------------------------------------------------------------------------------------------------------------|
    return read(srnm).collection(response['database'])

# |====================================================================================================================|
# | TEST READ DOCUMENT |===============================================================================================|
# |====================================================================================================================|
@bp.route("/test-read-document", methods=["GET"])
@required_token
@Model.read_document
@IAM.check_permission("read", "especific")
def test_read_document() -> tuple[list[dict] | str, int]:
    # GET USERNAME AND JSON REQUEST |----------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    response: dict[str] = request.json
    # |----------------------------------------------------------------------------------------------------------------|
    return read(srnm).document(response['database'], response['collection'], response['filter'])

# |====================================================================================================================|
# | TEST UPDATE DOCUMENT |=============================================================================================|
# |====================================================================================================================|
@bp.route("/test-update-document", methods=["PUT"])
@required_token
@Model.update_document
@IAM.check_permission("update", "especific")
def test_update_document() -> tuple[str, int]:
    # GET USERNAME AND JSON REQUEST |----------------------------------------------------------------------------------|
    srnm: str = IPToken.Tools.get_username_per_token(request.headers.get("Authorization"))
    response: dict[str] = request.json
    # |----------------------------------------------------------------------------------------------------------------|
    return update(srnm).document(response['database'], response['collection'], response['_id'], response['update'])