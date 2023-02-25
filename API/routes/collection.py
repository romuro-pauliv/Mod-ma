# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                           API.routes.collection.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, update, delete
from API.iam import Privileges
from API.identity.check_permission import IAM as CheckIAM
from API.models.routes.collection.decorators import Model
from API.secure.token.IPT_token import required_token

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

# | Blueprint |--------------------------------------------------------------------------------------------------------|
bp = Blueprint('collection', __name__, url_prefix='/collection')
# |--------------------------------------------------------------------------------------------------------------------|

# | Privileges |-------------------------------------------------------------------------------------------------------|
privileges_add = Privileges("admin").Add()
# |--------------------------------------------------------------------------------------------------------------------|

@bp.route("/", methods=["POST"])
@required_token
@Model.Create.collection
@CheckIAM.check_permission("create", "collection")
@privileges_add.collection
def create_collection() -> tuple[dict[str], int]:
    return create().collection(request.json["database"], request.json["collection"])


@bp.route("/", methods=["GET"])
@required_token
@Model.Read.collection
@CheckIAM.check_permission("read", "collection")
def read_collection() -> tuple[list[str] | dict[str], int]:
    return read().collection(request.json["database"])


@bp.route("/", methods=["DELETE"])
@required_token
@Model.Delete.collection
@CheckIAM.check_permission("delete", "collection")
def delete_collection() -> tuple[dict[str], int]:
    return delete().collection(request.json["database"], request.json["collection"])
