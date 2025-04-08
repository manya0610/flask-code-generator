


from src.code_generator.crud_generator import CRUDGenerator
from src.code_generator.exception_generator import ExceptionGenerator
from src.code_generator.flask_server_generator import FlaskServerGenerator
import os

class ProjectGenerator:
    project_name: str
    _crud_generator_list: list[CRUDGenerator] = []
    _flask_server_generator: FlaskServerGenerator
    _exception_generator: ExceptionGenerator

    def __init__(self, project_name:str):
        self.project_name = project_name

        self._exception_generator = ExceptionGenerator()
        self.exception_folder:str = "exceptions"
        self.exception_file:str = "exceptions"

        self._flask_server_generator = FlaskServerGenerator(self._crud_generator_list)

        
        self.flask_server_file:str = "flask_server"
        self.flask_server_folder:str = "flask_server"

        os.makedirs(self.project_name)
        os.makedirs(f"{self.project_name}/repo")
        os.makedirs(f"{self.project_name}/service")
        os.makedirs(f"{self.project_name}/controller")
        os.makedirs(f"{self.project_name}/flask_server")
        os.makedirs(f"{self.project_name}/exceptions")
        os.makedirs(f"{self.project_name}/database")



    def flask_server_file_generator(self) -> None:
        with open(f"{self.project_name}/{self.flask_server_folder}/{self.flask_server_file}.py", "w", encoding="utf-8") as f:
            f.write(self._flask_server_generator.app_generator())

    def exceptions_file_generator(self) -> None:
        with open(f"{self.project_name}/{self.exception_folder}/{self.exception_file}.py", "w", encoding="utf-8") as f:
            f.write(self._exception_generator.database_exceptions_generator())
            f.write(self._exception_generator.request_exceptions_generator())
    

