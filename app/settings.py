import os
from dotenv import load_dotenv


class Config:

    def __init__(self):

        if os.getenv("PRODUCTION", False):
            self.PRODUCTION = True
        else:
            self.PRODUCTION = False
            load_dotenv()

        self.DB_USER = self.get_env("DB_USER")
        self.DB_NAME = self.get_env("DB_NAME")
        self.DB_HOST = self.get_env("DB_HOST")
        self.DB_PORT = self.get_env("DB_PORT")
        self.DB_PASSWORD = self.get_env("DB_PASSWORD")

        self.DB_URL = f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

        self.DB_ECHO = self.get_bool("DB_ECHO")

        self.EMAIL_SENDER = self.get_env("EMAIL_SENDER")
        self.EMAIL_SERVER_HOST = self.get_env("EMAIL_SERVER_HOST")
        self.EMAIL_SERVER_PORT = self.get_int("EMAIL_SERVER_PORT")
        self.EMAIL_PASSWORD = self.get_env("EMAIL_PASSWORD")
        self.EMAIL_USERNAME = self.get_env("EMAIL_USERNAME")

        self.HOST_DOMAIN = self.get_env("HOST_DOMAIN")
        self.SECRET_KEY = self.get_env("SECRET_KEY")
        self.SECURE_COOKIES = self.get_bool("SECURE_COOKIES")

    def get_env(self, variable_name) -> str:
        variable = os.getenv(variable_name)

        if variable is not None:
            return variable
        else:
            self.__raise_undefined_error(variable_name)

    def get_int(self, variable_name) -> int:
        variable = self.get_env(variable_name)

        return int(variable)

    def get_bool(self, variable_name) -> bool:
        variable = self.get_env(variable_name).lower()

        if variable in ("true", "yes", "1", "sim, por favor :)"):
            return True
        else:
            return False

    def __raise_undefined_error(self, missing_var):
        raise Exception(
            f"The environment variable '{missing_var}' is undefined in .env!"
        )


config = Config()
