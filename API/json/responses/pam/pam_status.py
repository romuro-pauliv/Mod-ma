# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                               API.json.reponses.pam.pam_request.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
from API.status import *
from API.json.tools.tools import response_structure
from typing import Any
# |--------------------------------------------------------------------------------------------------------------------|

class Responses(object):
    class R4XX(object):
        @staticmethod
        def only_json() -> tuple[dict[str], int]:
            return response_structure("ONLY JSON ARE ALLOWED", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def key_error() -> tuple[dict[str], int]:
            return response_structure("BAD REQUEST - KEY ERROR", HTTP_400_BAD_REQUEST)

        @staticmethod
        def user_not_found(username: str) -> tuple[dict[str], int]:
            return response_structure(f"USER [{username}] NOT FOUND", HTTP_404_NOT_FOUND)
        
        @staticmethod
        def invalid_command(command: str) -> tuple[dict[str], int]:
            return response_structure(f"INVALID COMMAND - [{command}]", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def invalid_crud_method(crud_method: str) -> tuple[dict[str], int]:
            return response_structure(f"INVALID CRUD METHOD - [{crud_method}]", HTTP_400_BAD_REQUEST)
        
        @staticmethod
        def invalid_object_type_arguments() -> tuple[dict[str], int]:
            return response_structure("INVALID OBJECT TYPE IN [ARGUMENTS] FIELD", HTTP_400_BAD_REQUEST)

        @staticmethod
        def invalid_item_in_arguments(item: Any) -> tuple[dict[str], int]:
            return response_structure(
                f"INVALID ITEM TYPE IN ARGUMENTS - ONLY STRING OR LIST - [{str(item)}]", HTTP_400_BAD_REQUEST
            )
        
        @staticmethod
        def invalid_path(path_: str) -> tuple[dict[str], int]:
            return response_structure(f"INVALID PATH [{path_}]", HTTP_400_BAD_REQUEST)

        @staticmethod
        def invalid_path_error_len_list(list_: list[str]) -> tuple[dict[str], int]:
            return response_structure(
                f"INVALID PATH - THE LIST MUST HAVE ONLY 2 ARGUMENTS [{str(list_)}]", HTTP_400_BAD_REQUEST
                )
        
        @staticmethod
        def invalid_item_in_list(item: Any) -> tuple[dict[str], int]:
            return response_structure(
                f"INVALID OBJECT TYPE IN LIST - {[str(item)]} - MUST BE A STRING", HTTP_400_BAD_REQUEST
            )
        
        @staticmethod
        def database_not_found(database_name: str) -> tuple[dict[str], int]:
            return response_structure(f"DATABASE [{database_name}] NOT FOUND", HTTP_404_NOT_FOUND)
        
        @staticmethod
        def collection_not_found(collection_name: str) -> tuple[dict[str], int]:
            return response_structure(f"DATABASE [{collection_name}] NOT FOUND", HTTP_404_NOT_FOUND)
        
        @staticmethod
        def unauthorized_request(username: str) -> tuple[dict[str], int]:
            return response_structure(f"FORBIDDEN - USER [{username}] UNAUTHORIZED", HTTP_403_FORBIDDEN)
        
    class R2XX(object):
        def json_valid() -> tuple[str, int]:
            return "JSON VALID", HTTP_202_ACCEPTED
        
        def user_valid() -> tuple[str, int]:
            return "USER VALID", HTTP_202_ACCEPTED
        
        def command_valid() -> tuple[str, int]:
            return "COMMAND VALID", HTTP_202_ACCEPTED
        
        def crud_method_valid() -> tuple[str, int]:
            return "CRUD METHOD VALID", HTTP_202_ACCEPTED

        def arguments_valid() -> tuple[dict[str], int]:
            return "ARGUMENTS VALID", HTTP_202_ACCEPTED
        
        def update_privileges() -> tuple[dict[str], int]:
            return response_structure("UPDATE PRIVILEGES", HTTP_202_ACCEPTED)