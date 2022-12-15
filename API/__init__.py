# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# +--------------------------------------------------------------------------------------------------------------------+
import os
from flask import Flask
from typing import Union

from .database.crud import create, read, drop
# +--------------------------------------------------------------------------------------------------------------------+


def create_app(test_config: Union[bool, None] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=os.environ['MONGO_URI']
    )

    # test config |----------------------------------------------------------------------------------------------------|
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # |----------------------------------------------------------------------------------------------------------------|

    # Ensure the instance folder exists |------------------------------------------------------------------------------|
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # |----------------------------------------------------------------------------------------------------------------|
    
    # A simple page that say hello |-----------------------------------------------------------------------------------|
    @app.route("/create/document")
    def create_test() -> tuple:

        doc: dict[str, any] = {
            "mode": "modo",
            "method": "method"
        }

        return create.document(database='testing', collection='hello', document=doc)
    # |----------------------------------------------------------------------------------------------------------------|


    return app
