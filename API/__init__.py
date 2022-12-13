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
# +--------------------------------------------------------------------------------------------------------------------+


def create_app(test_config: Union[bool, None] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=os.environ['MONGO_URI']
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists |------------------------------------------------------------------------------|
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # |----------------------------------------------------------------------------------------------------------------|
    
    # A simple page that say hello |-----------------------------------------------------------------------------------|
    @app.route('/hello')
    def hello() -> str:
        return os.environ["MONGO_URI"]
    # |----------------------------------------------------------------------------------------------------------------|

    from . import db

    @app.route("/db")
    def testing() -> str:
        return db.get_db().list_database_names()


    return app
