
from flask import Blueprint

bp = Blueprint('test', __name__, url_prefix='/test')

@bp.route("/test")
def test() -> dict[str]:
    return {"hello": "world"}