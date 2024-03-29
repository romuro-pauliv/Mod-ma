# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                    API.__init__.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|


# | Imports |----------------------------------------------------------------------------------------------------------+
import os
from flask import Flask
from typing import Union
import asyncio
# +--------------------------------------------------------------------------------------------------------------------+


def create_app(test_config: Union[bool, None] = None) -> Flask:
    # create and configure the app |-----------------------------------------------------------------------------------|
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=os.environ['MONGO_URI']
    )
    # |----------------------------------------------------------------------------------------------------------------|

    # test config |----------------------------------------------------------------------------------------------------|
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    # |----------------------------------------------------------------------------------------------------------------|
    
    # auth blueprint |-------------------------------------------------------------------------------------------------|
    from .routes import auth
    app.register_blueprint(auth.bp)
    # |----------------------------------------------------------------------------------------------------------------|

    # test blueprint |-------------------------------------------------------------------------------------------------|
    from .routes import tests
    app.register_blueprint(tests.bp)
    # |----------------------------------------------------------------------------------------------------------------|

    # database blueprint |---------------------------------------------------------------------------------------------|
    from .routes import database
    app.register_blueprint(database.bp)
    # |----------------------------------------------------------------------------------------------------------------|

    # collection blueprint |-------------------------------------------------------------------------------------------|
    from .routes import collection
    app.register_blueprint(collection.bp)
    # |----------------------------------------------------------------------------------------------------------------|
    
    # document blueprint |---------------------------------------------------------------------------------------------|
    from .routes import document
    app.register_blueprint(document.bp)
    # |----------------------------------------------------------------------------------------------------------------|


    return app

