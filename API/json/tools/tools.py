# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                         API.json.reponses.tools.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | Imports |----------------------------------------------------------------------------------------------------------|
import datetime
# |--------------------------------------------------------------------------------------------------------------------|

def response_structure(response: str, status_code: int) -> tuple[dict, int]:
    json_response: dict[str | dict[str]] = {
        "date": str(f"UTC {datetime.datetime.utcnow()}"),
        "response": response,
        "status_code": str(status_code)
        }
    return json_response, status_code