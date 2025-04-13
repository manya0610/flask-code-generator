from typing import Any

from sqlalchemy import Column

from src.code_generator import constants
from src.code_generator.controller_generator import ControllerGenerator
from src.code_generator.database_model import DataBaseModel
from src.code_generator.repo_generator import RepoGenerator
from src.code_generator.service_generator import ServiceGenerator

class CRUDGenerator:
    database_model: DataBaseModel
    service_generator: ServiceGenerator
    repo_generator: RepoGenerator
    controller_generator: ControllerGenerator
    

    repo_file: str
    repo_folder: str
    service_file: str
    service_folder: str
    controller_file: str
    controller_folder: str

    def __init__(
        self, project_name:str, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ):

        self.project_name = project_name

        self.database_model = DataBaseModel(model_name, model_attributes, models_file)

        self.repo_generator = RepoGenerator(self.database_model)
        self.repo_file = self.database_model.model_name_snake_case + "_" + "repo"

        self.service_generator = ServiceGenerator(self.database_model, self.repo_file)
        self.service_file = self.database_model.model_name_snake_case + "_" + "service"

        self.controller_generator = ControllerGenerator(self.database_model, self.service_file)
        self.controller_file = self.database_model.model_name_snake_case + "_" + "controller"
        

    def repo_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.REPO_FOLDER}/{self.repo_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self.repo_generator.get_imports())
            f.write(self.repo_generator.list_query_generator())
            f.write(self.repo_generator.get_query_generator())
            f.write(self.repo_generator.create_query_generator())
            f.write(self.repo_generator.update_query_generator())
            f.write(self.repo_generator.delete_query_generator())

    def service_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.SERVICE_FOLDER}/{self.service_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self.service_generator.get_imports())
            f.write(self.service_generator.list_query_generator())
            f.write(self.service_generator.get_query_generator())
            f.write(self.service_generator.create_query_generator())
            f.write(self.service_generator.update_query_generator())
            f.write(self.service_generator.delete_query_generator())

    def controller_file_generator(self) -> None:
        with open(
            f"{self.project_name}/{constants.CONTROLLER_FOLDER}/{self.controller_file}.py", "w", encoding="utf-8"
        ) as f:
            f.write(self.controller_generator.get_imports())
            f.write(self.controller_generator.create_handler_generator())
            f.write(self.controller_generator.list_handler_generator())
            f.write(self.controller_generator.get_handler_generator())
            f.write(self.controller_generator.update_handler_generator())
            f.write(self.controller_generator.delete_handler_generator())
    




