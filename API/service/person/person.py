# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                              API.service.person.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# + imports +----------------------------------------------------------------------------------------------------------+
from API.db import create
from API.status import *
# |--------------------------------------------------------------------------------------------------------------------|

class LegalPerson(object):
    def __init__(self, username: str) -> None:
        self.username: str = username
    
    def create(self) -> None:
        pass

    def read(self) -> None:
        pass

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass