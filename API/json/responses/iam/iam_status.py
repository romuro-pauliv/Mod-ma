# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.json.reponses.iam.iam_request.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.tools.tools import response_structure
# |--------------------------------------------------------------------------------------------------------------------|

class Responses(object):
    class R4XX(object):
        @staticmethod
        def require_privileges_error(username: str) -> tuple[dict, int]:
            return response_structure(
                f"USER [{username}] REQUIRE PRIVILEGES", HTTP_403_FORBIDDEN
            )
        
        @staticmethod
        def db_or_coll_not_found(database: str, collection: str) -> tuple[dict, int]:
            return response_structure(
                f"DATABASE [{database}] OR COLLECTION [{collection}] NOT FOUND", HTTP_404_NOT_FOUND
            )
        
        @staticmethod
        def internal_error_structure() -> tuple[str, int]:
            return "BAD REQUEST - STRUCTURE", HTTP_400_BAD_REQUEST