import os

from flask_code_generator import constants
from flask_code_generator.constant_generator import ConstantGenerator
from flask_code_generator.crud_generator import CRUDGenerator
from flask_code_generator.database_generator import DatabaseGenerator
from flask_code_generator.database_script_generator import DatabaseScriptGenerator
from flask_code_generator.exception_generator import ExceptionGenerator
from flask_code_generator.flask_server_generator import FlaskServerGenerator


class ProjectGenerator:
    project_name: str
    constant_generator: ConstantGenerator
    crud_generator_list: list[CRUDGenerator] = []
    database_generator: DatabaseGenerator
    database_script_generator: DatabaseScriptGenerator
    exception_generator: ExceptionGenerator
    flask_server_generator: FlaskServerGenerator

    def __init__(self, project_name: str):
        self.project_name = project_name

        self.exception_generator = ExceptionGenerator()
        self.constant_generator = ConstantGenerator()
        self.database_generator = DatabaseGenerator()
        self.database_script_generator = DatabaseScriptGenerator(self.project_name)

        self.flask_server_generator = FlaskServerGenerator(self.crud_generator_list)

        os.makedirs(self.project_name)
        os.makedirs(f"{self.project_name}/{constants.REPO_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.SERVICE_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.CONTROLLER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.FLASK_SERVER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.EXCEPTIONS_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.DATABASE_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.CONSTANTS_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.SCRIPTS_FOLDER}")

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

    def database_script_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.SCRIPTS_FOLDER}/db_scripts.py",
            "w",
            encoding="utf-8",
        ) as f:
            f.write(self.database_script_generator.database_script_generator())
