# +--------------------------------------------------------------------------------------------------------------------|
# |                                                                                                        CLI.exec.py |
# |                                                                                             Author: Pauliv, Rômulo |
# |                                                                                          email: romulopauliv@bk.ru |
# |                                                                                                    encoding: UTF-8 |
# +--------------------------------------------------------------------------------------------------------------------|

# | imports |----------------------------------------------------------------------------------------------------------|
from typing import Union
from colorama import Fore, Style
import os

from commands.exit_ import close
from commands.auth import auth
from commands.read import read

from data.command_name import *
# |--------------------------------------------------------------------------------------------------------------------|


class exec(object):
    def __init__(self) -> None:
        self.username: Union[str, None] = None
        self.token: Union[str, None] = None
        self.prefix: str = "|> "
    
    def update_prefix(self) -> None:
        if self.username is not None:
            self.prefix: str = str(Fore.MAGENTA + f"@{self.username}" + Style.RESET_ALL + " |> ")
        
    def commands_auth(self, cmd: str) -> None:
            # | LOGIN |================================================================================================|
            if cmd == COMMAND_LOGIN:
                val: Union[dict[str], None] = auth.login()
                if isinstance(val, dict):
                    self.username: str = val["username"]
                    self.token: str = val['token']
                    self.update_prefix()
            # |========================================================================================================|
            
            # | REGISTER |=============================================================================================|
            if cmd == COMMAND_REGISTER:
                auth.register()
            # |========================================================================================================|

            # | LOGOUT |===============================================================================================|
            if cmd == COMMAND_LOGOUT:
                self.username: None = None
                self.token: None = None
                os.system("clear")
                self.prefix: str = "|> "
            # |========================================================================================================|
    
    def commands_read(self, cmd: str) -> None:
        # DATABASE |===================================================================================================|
        if cmd == COMMAND_READ_DATABASE:
            read.database(self.token)
        # |============================================================================================================|

        # COLLECTION |=================================================================================================|
        if cmd == COMMAND_READ_COLLECTION:
            read.collection(self.token)
        # |============================================================================================================|

    def init(self) -> None:
        while True:
            command: str = input(self.prefix)

            self.commands_auth(command)
            self.commands_read(command)

            if command == COMMAND_EXIT:
                close()