


from src.code_generator.crud_generator import CRUDGenerator
from src.code_generator.exception_generator import ExceptionGenerator
from src.code_generator.flask_server_generator import FlaskServerGenerator
from src.code_generator import constants
import os

class ProjectGenerator:
    project_name: str
    crud_generator_list: list[CRUDGenerator] = []
    _flask_server_generator: FlaskServerGenerator
    _exception_generator: ExceptionGenerator

    def __init__(self, project_name:str):
        self.project_name = project_name

        self._exception_generator = ExceptionGenerator()

        self._flask_server_generator = FlaskServerGenerator(self.crud_generator_list)

        os.makedirs(self.project_name)
        os.makedirs(f"{self.project_name}/{constants.REPO_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.SERVICE_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.CONTROLLER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.FLASK_SERVER_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.EXCEPTIONS_FOLDER}")
        os.makedirs(f"{self.project_name}/{constants.DATABASE_FOLDER}")



    def flask_server_file_generator(self) -> None:
        with open(f"{self.project_name}/{constants.FLASK_SERVER_FOLDER}/{constants.FLASK_SERVER_FILE}.py", "w", encoding="utf-8") as f:
            f.write(self._flask_server_generator.app_generator())

    def exceptions_file_generator(self) -> None:
        with open(f"{self.project_name}/{constants.EXCEPTIONS_FOLDER}/{"exceptions"}.py", "w", encoding="utf-8") as f:
            f.write(self._exception_generator.database_exceptions_generator())
            f.write(self._exception_generator.request_exceptions_generator())
    

