# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.document.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, update, delete
from API.iam import IAM
from API.models.routes.document.decorators import Model
from API.secure.token.IPT_token import required_token

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

# | Blueprint |--------------------------------------------------------------------------------------------------------|
bp = Blueprint('document', __name__, url_prefix='/document')
# |--------------------------------------------------------------------------------------------------------------------|


@bp.route("/", methods=["POST"])
@required_token
@Model.Create.document
@IAM.check_permission("create", "especific")
def create_document() -> tuple[dict[str], int]:
    return create().document(request.json["database"], request.json["collection"], request.json["document"])


@bp.route("/", methods=["GET"])
@required_token
@Model.Read.document
@IAM.check_permission("read", "especific")
def read_document() -> tuple[list[dict] | dict[str], int]:
    return read().document(request.json["database"], request.json["collection"], request.json["filter"])


@bp.route("/", methods=["PUT"])
@required_token
@Model.Update.document
@IAM.check_permission("update", "especific")
def update_document() -> tuple[dict[str], int]:
    return update().document(
        request.json["database"], request.json["collection"], request.json["_id"], request.json["update"])


@bp.route("/", methods=["DELETE"])
@required_token
@Model.Delete.document
@IAM.check_permission("delete", "especific")
def delete_document() -> tuple[dict[str], int]:
    return delete().document(request.json["database"], request.json["collection"], request.json["_id"])
