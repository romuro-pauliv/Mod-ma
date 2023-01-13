# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                        CLI.exec.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from typing import Union
from colorama import Fore, Style

from commands.exit_ import close
from commands.auth import auth

from command_name import *
# |--------------------------------------------------------------------------------------------------------------------|


class exec(object):
    def __init__(self) -> None:
        self.username: Union[str, None] = None
        self.token: Union[str, None] = None
        self.prefix: str = "|> "
    
    def update_prefix(self) -> None:
        if self.username is not None:
            self.prefix: str = str(Fore.MAGENTA + f"@{self.username}" + Style.RESET_ALL + " |> ")

    def init(self) -> None:
        while True:
            command: str = input(self.prefix)

            if command == COMMAND_LOGIN:
                val: dict[str] = auth.login()
                self.username: str = val["username"]
                self.token: str = val['token']
                self.update_prefix()
            
            if command == "--token":
                print(self.token)


            if command == COMMAND_EXIT:
                close()