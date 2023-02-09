# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                             API.routes.database.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# imports |------------------------------------------------------------------------------------------------------------|
from API.status import *
from API.db import create, read, update, delete
from API.iam import IAM, Privileges

from API.models.routes.tests.decorators import Model

from API.secure.token.IPT_token import required_token, IPToken

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
def create_database() -> tuple[str, int]:
    return create().database(request.json["database"])

