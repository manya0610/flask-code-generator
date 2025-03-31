from typing import Any

from sqlalchemy import Column

from src.code_generator.controller_generator import ControllerGenerator
from src.code_generator.database_model import DataBaseModel
from src.code_generator.flask_server_generator import FlaskServerGenerator
from src.code_generator.repo_generator import RepoGenerator
from src.code_generator.service_generator import ServiceGenerator
from src.code_generator.exception_generator import ExceptionGenerator

class CodeGenerator():
    _database_model: DataBaseModel
    _service_generator: ServiceGenerator
    _repo_generator: RepoGenerator
    _flask_server_generator: FlaskServerGenerator
    _controller_generator: ControllerGenerator
    _exception_generator: ExceptionGenerator

    repo_file: str
    service_file: str
    controller_file: str
    exception_file: str

    def __init__(
        self, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ):
        self._database_model = DataBaseModel(model_name, model_attributes, models_file)

        self._repo_generator = RepoGenerator(self._database_model)
        self.repo_file = self._database_model.model_name_snake_case + "_" + "repo"

        self._service_generator = ServiceGenerator(self._database_model, self.repo_file)
        self.service_file = self._database_model.model_name_snake_case + "_" + "service"

        self._controller_generator = ControllerGenerator(self._database_model, self.service_file)
        self.controller_file = self._database_model.model_name_snake_case + "_" + "controller"
        
        self._flask_server_generator = FlaskServerGenerator(self._database_model, self.controller_file)
        self.flask_server_file = "flask_server"

        self._exception_generator = ExceptionGenerator(self._database_model)
        self.exception_file =  "exceptions"

    def repo_file_generator(self) -> None:
        with open(
            f"{self.repo_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._repo_generator.get_imports())
            f.write(self._repo_generator.list_query_generator())
            f.write(self._repo_generator.get_query_generator())
            f.write(self._repo_generator.create_query_generator())
            f.write(self._repo_generator.update_query_generator())
            f.write(self._repo_generator.delete_query_generator())

    def service_file_generator(self) -> None:
        with open(
            f"{self.service_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._service_generator.get_imports())
            f.write(self._service_generator.list_query_generator())
            f.write(self._service_generator.get_query_generator())
            f.write(self._service_generator.create_query_generator())
            f.write(self._service_generator.update_query_generator())
            f.write(self._service_generator.delete_query_generator())

    def controller_file_generator(self) -> None:
        with open(
            f"{self.controller_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._controller_generator.get_imports())
            f.write(self._controller_generator.create_handler_generator())
            f.write(self._controller_generator.list_handler_generator())
            f.write(self._controller_generator.get_handler_generator())
            f.write(self._controller_generator.update_handler_generator())
            f.write(self._controller_generator.delete_handler_generator())
    
    def flask_server_file_generator(self) -> None:
        with open(f"{self.flask_server_file}.py", "w", encoding="utf-8") as f:
            f.write(self._flask_server_generator.app_generator())

    def exceptions_file_generator(self) -> None:
        with open(f"{self.exception_file}.py", "w", encoding="utf-8") as f:
            f.write(self._exception_generator.database_exceptions_generator())
            f.write(self._exception_generator.request_exceptions_generator())



