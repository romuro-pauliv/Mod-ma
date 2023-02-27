# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, delete
from API.identity.check_permission import IAM as CheckIAM
from API.identity.add import IAM as AddIAM
from API.models.routes.database.decorators import Model
from API.secure.token.IPT_token import required_token

from flask import Blueprint, request
# |--------------------------------------------------------------------------------------------------------------------|

# | Blueprint |--------------------------------------------------------------------------------------------------------|
bp = Blueprint('database', __name__, url_prefix='/database')
# |--------------------------------------------------------------------------------------------------------------------|

# | Privileges |-------------------------------------------------------------------------------------------------------|
add_privileges = AddIAM.Add("admin")
# |--------------------------------------------------------------------------------------------------------------------|

@bp.route('/', methods=["POST"])
@required_token
@Model.Create.database
@CheckIAM.check_permission("create", "database")
@add_privileges.new_database
def create_database() -> tuple[dict[str], int]:
    return create().database(request.json["database"])


@bp.route('/', methods=["GET"])
@required_token
@CheckIAM.check_permission("read", "database")
def read_database() -> tuple[list[str] | dict[str], int]:
    return read().database()


@bp.route('/', methods=['DELETE'])
@required_token
@Model.Delete.database
@CheckIAM.check_permission("delete", "database")
def delete_database() -> tuple[dict[str], int]:
    return delete().database(request.json["database"])