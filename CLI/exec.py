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
from commands.create import create
from commands.update import update
from commands.delete import delete

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
    
    def commands_create(self, cmd: str) -> None:
        # DATABASE |===================================================================================================|
        if cmd == COMMAND_CREATE_DATABASE:
            create.database(self.token)
        # =============================================================================================================|
        
        # COLLECTION |=================================================================================================|
        if cmd == COMMAND_CREATE_COLLECTION:
            create.collection(self.token)
        # |============================================================================================================|
        
        # DOCUMENT |===================================================================================================|
        if cmd == COMMAND_CREATE_DOCUMENT:
            create.document(self.token)
        # |============================================================================================================|
    
    def commands_read(self, cmd: str) -> None:
        # DATABASE |===================================================================================================|
        if cmd == COMMAND_READ_DATABASE:
            read.database(self.token)
        # |============================================================================================================|

        # COLLECTION |=================================================================================================|
        if cmd == COMMAND_READ_COLLECTION:
            read.collection(self.token)
        # |============================================================================================================|
        
        if cmd == COMMAND_READ_DOCUMENT:
            read.documents(self.token)
    
    def commands_update(self, cmd: str) -> None:
        # DOCUMENT |===================================================================================================|
        if cmd == COMMAND_UPDATE_DOCUMENT:
            update.document(self.token)
        # |============================================================================================================|

    def commands_delete(self, cmd: str) -> None:
        # DATABASE |===================================================================================================|
        if cmd == COMMAND_DELETE_DATABASE:
            delete.database(self.token)
        # |============================================================================================================|
        
        # COLLECTION |=================================================================================================|
        if cmd == COMMAND_DELETE_COLLECTION:
            delete.collection(self.token)
        # |============================================================================================================|
                
        # DOCUMENT |===================================================================================================|
        if cmd == COMMAND_DELETE_DOCUMENT:
            delete.document(self.token)
        # |============================================================================================================|


    def init(self) -> None:
        while True:
            command: str = input(self.prefix)

            self.commands_auth(command)
            
            self.commands_read(command)
            self.commands_create(command)
            self.commands_update(command)
            self.commands_delete(command)
            
            if command == COMMAND_EXIT:
                close()