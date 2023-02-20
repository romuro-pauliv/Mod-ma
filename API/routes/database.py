# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, delete
from API.iam import IAM, Privileges
from API.models.routes.database.decorators import Model
from API.secure.token.IPT_token import required_token

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

# | Blueprint |--------------------------------------------------------------------------------------------------------|
bp = Blueprint('database', __name__, url_prefix='/database')
# |--------------------------------------------------------------------------------------------------------------------|

# | Privileges |-------------------------------------------------------------------------------------------------------|
privileges_add = Privileges("admin").Add()
# |--------------------------------------------------------------------------------------------------------------------|

@bp.route('/', methods=["POST"])
@required_token
@Model.Create.database
@IAM.check_permission("create", "database")
@privileges_add.database
def create_database() -> tuple[dict[str], int]:
    return create().database(request.json["database"])


@bp.route('/', methods=["GET"])
@required_token
@IAM.check_permission("read", "database")
def read_database() -> tuple[list[str] | dict[str], int]:
    return read().database()


@bp.route('/', methods=['DELETE'])
@required_token
@Model.Delete.database
@IAM.check_permission("delete", "database")
def delete_database() -> tuple[dict[str], int]:
    return delete().database(request.json["database"])