from typing import Any

from sqlalchemy import Column

from src.code_generator.controller_generator import ControllerGenerator
from src.code_generator.database_model import DataBaseModel
from src.code_generator.repo_generator import RepoGenerator
from src.code_generator.service_generator import ServiceGenerator

class CRUDGenerator:
    _database_model: DataBaseModel
    _service_generator: ServiceGenerator
    _repo_generator: RepoGenerator
    _controller_generator: ControllerGenerator
    

    repo_file: str
    repo_folder: str
    service_file: str
    service_folder: str
    controller_file: str
    controller_folder: str
    project_name: str

    def __init__(
        self, project_name:str, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ):
        self.project_name = project_name
        self._database_model = DataBaseModel(model_name, model_attributes, models_file)

        self._repo_generator = RepoGenerator(self._database_model)
        self.repo_file = self._database_model.model_name_snake_case + "_" + "repo"
        self.repo_folder = "repo"

        self._service_generator = ServiceGenerator(self._database_model, self.repo_file, self.repo_folder)
        self.service_file = self._database_model.model_name_snake_case + "_" + "service"
        self.service_folder = "service"

        self._controller_generator = ControllerGenerator(self._database_model, self.service_file, self.service_folder)
        self.controller_file = self._database_model.model_name_snake_case + "_" + "controller"
        self.controller_folder = "controller"

    def repo_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{self.repo_folder}/{self.repo_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._repo_generator.get_imports())
            f.write(self._repo_generator.list_query_generator())
            f.write(self._repo_generator.get_query_generator())
            f.write(self._repo_generator.create_query_generator())
            f.write(self._repo_generator.update_query_generator())
            f.write(self._repo_generator.delete_query_generator())

    def service_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{self.service_folder}/{self.service_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._service_generator.get_imports())
            f.write(self._service_generator.list_query_generator())
            f.write(self._service_generator.get_query_generator())
            f.write(self._service_generator.create_query_generator())
            f.write(self._service_generator.update_query_generator())
            f.write(self._service_generator.delete_query_generator())

    def controller_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{self.controller_folder}/{self.controller_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._controller_generator.get_imports())
            f.write(self._controller_generator.create_handler_generator())
            f.write(self._controller_generator.list_handler_generator())
            f.write(self._controller_generator.get_handler_generator())
            f.write(self._controller_generator.update_handler_generator())
            f.write(self._controller_generator.delete_handler_generator())
    




