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
from flask_pymongo import PyMongo
# +--------------------------------------------------------------------------------------------------------------------+


def create_app(test_config: Union[bool, None] = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        MONGO_URI=os.environ['MONGO_URI']
    )

    # Ensure the instance folder exists |------------------------------------------------------------------------------|
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    # |----------------------------------------------------------------------------------------------------------------|
    
    # A simple page that say hello |-----------------------------------------------------------------------------------|
    print("Hello Route")
    @app.route('/hello')
    def hello() -> str:
        return os.environ["MONGO_URI"]
    # |----------------------------------------------------------------------------------------------------------------|

    return app
