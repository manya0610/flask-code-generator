import os

from src.code_generator import constants
from src.code_generator.constant_generator import ConstantGenerator
from src.code_generator.crud_generator import CRUDGenerator
from src.code_generator.database_generator import DatabaseGenerator
from src.code_generator.exception_generator import ExceptionGenerator
from src.code_generator.flask_server_generator import FlaskServerGenerator


class ProjectGenerator:
    project_name: str
    crud_generator_list: list[CRUDGenerator] = []
    flask_server_generator: FlaskServerGenerator
    exception_generator: ExceptionGenerator
    constant_generator: ConstantGenerator
    database_generator: DatabaseGenerator

    def __init__(self, project_name: str):
        self.project_name = project_name

        self.exception_generator = ExceptionGenerator()
        self.constant_generator = ConstantGenerator()
        self.database_generator = DatabaseGenerator()

        self.flask_server_generator = FlaskServerGenerator(self.crud_generator_list)

        os.makedirs(self.project_name)
        os.makedirs(f"{self.project_name}/{constants.REPO_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.SERVICE_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.CONTROLLER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.FLASK_SERVER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.EXCEPTIONS_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.DATABASE_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.CONSTANTS_FOLDER}")

    def init_file_generator(self):
        with open(f"{self.project_name}/__init__.py", "w", encoding="utf-8") as f:
            f.write("")

    def flask_server_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.FLASK_SERVER_FOLDER}/{constants.FLASK_SERVER_FILE}.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.flask_server_generator.app_generator())

    def exceptions_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.EXCEPTIONS_FOLDER}/{'exceptions'}.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.exception_generator.database_exceptions_generator())
            f.write(self.exception_generator.request_exceptions_generator())

    def constants_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.CONSTANTS_FOLDER}/{constants.CONSTANTS_ERROR_MESSAGE_FILE}.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.constant_generator.error_message_constants_generator())

    def database_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.DATABASE_FOLDER}/{constants.DATABASE_FILE}.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.database_generator.database_generator())
