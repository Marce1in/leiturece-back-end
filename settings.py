import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        self.__db_url = os.getenv("DB_URL")
        self.__db_echo = os.getenv("DB_ECHO")

    def get_db_url(self) -> str:
        if type(self.__db_url) != str:
            raise Exception("DATABASE URL NOT DEFINDED")

        return self.__db_url

    def get_db_echo(self) -> bool:
        if type(self.__db_echo) != str:
            raise Exception("DATABASE ECHO NOT DEFINED")
        elif self.__db_echo.lower() in ("1", "true", "yes"):
            return True
        else:
            return False

config = Config()
