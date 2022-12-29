# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                 API.routes.test.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.auth import required_token
from API.db import create
from API.models.route_test import Model

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
def test_create_database() -> tuple[str, int]:
    database_name: str = request.json["database"]
    return create.database(database_name)
# |--------------------------------------------------------------------------------------------------------------------|

# test create collection |---------------------------------------------------------------------------------------------|
@bp.route("/test-create-collection", methods=['POST'])
@required_token
@Model.create_collection
def test_create_collection() -> tuple[str, int]:
    response: dict[str, str] = request.json
    return create.collection(response['database'], response['collection'])
# |--------------------------------------------------------------------------------------------------------------------|

@bp.route("/test-create-document", methods=["POST"])
@required_token
@Model.create_document
def test_create_document() -> tuple[str, int]:
    response: dict[str, str | dict] = request.json
    return create.document(response['database'], response['collection'], response['document'])

