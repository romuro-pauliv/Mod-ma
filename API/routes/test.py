# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.test.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.auth import required_token, get_username_per_token
from API.db import create
from API.models.route_test import Model
from API.iam import IAM

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

bp = Blueprint('test', __name__, url_prefix='/tests')

# test token |---------------------------------------------------------------------------------------------------------|
@bp.route('/test-token', methods=['POST'])
@required_token
def test_token() -> tuple[str, int]:
    return 'TEST OK', HTTP_202_ACCEPTED
# |--------------------------------------------------------------------------------------------------------------------|

# test create database |-----------------------------------------------------------------------------------------------|
@bp.route('/test-create-database', methods=['POST'])
@required_token
@Model.create_database
@IAM.check_permission("create", "database")
def test_create_database() -> tuple[str, int]:
    
    # GET USERNAME AND DATABASE NAME |---------------------------------------------------------------------------------|
    srnm: str = get_username_per_token(request.headers.get("Authorization"))
    database_name_json: str = request.json["database"]
    # |----------------------------------------------------------------------------------------------------------------|

    return create(srnm).database(database_name_json)
# |--------------------------------------------------------------------------------------------------------------------|

# test create collection |---------------------------------------------------------------------------------------------|
@bp.route("/test-create-collection", methods=['POST'])
@required_token
@Model.create_collection
@IAM.check_permission("create", "collection")
def test_create_collection() -> tuple[str, int]:

    # GET USERNAME AND JSON RESPONSE |---------------------------------------------------------------------------------|
    srnm: str = get_username_per_token(request.headers.get("Authorization"))
    response: dict[str, str] = request.json
    # |----------------------------------------------------------------------------------------------------------------|

    return create(srnm).collection(response['database'], response['collection'])
# |--------------------------------------------------------------------------------------------------------------------|

@bp.route("/test-create-document", methods=["POST"])
@required_token
@Model.create_document
def test_create_document() -> tuple[str, int]:
    response: dict[str, str | dict] = request.json
    return create.document(response['database'], response['collection'], response['document'])

