from typing import Any

from sqlalchemy import Column

from src.code_generator.database_model import DataBaseModel
from src.code_generator.repo_generator import RepoGenerator
from src.code_generator.service_generator import ServiceGenerator


class CodeGenerator(DataBaseModel):
    _service_generator: ServiceGenerator
    _repo_generator: RepoGenerator

    def __init__(
        self, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ):
        super().__init__(model_name, model_attributes, models_file)
        self._service_generator = ServiceGenerator(
            model_name, model_attributes, models_file
        )
        self._repo_generator = RepoGenerator(model_name, model_attributes, models_file)

    def service_file_generator(self) -> None:
        with open(
            f"{self.model_name_snake_case.lower()}_service.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._service_generator.get_imports())
            f.write(self._service_generator.get_all_query_generator())
            f.write(self._service_generator.get_query_generator())
            f.write(self._service_generator.create_query_generator())
            f.write(self._service_generator.update_query_generator())
            f.write(self._service_generator.delete_query_generator())

    def repo_file_generator(self) -> None:
        with open(
            f"{self.model_name_snake_case.lower()}_repo.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._repo_generator.get_imports())
            f.write(self._repo_generator.list_query_generator())
            f.write(self._repo_generator.get_query_generator())
            f.write(self._repo_generator.create_query_generator())
            f.write(self._repo_generator.update_query_generator())
            f.write(self._repo_generator.delete_query_generator())
