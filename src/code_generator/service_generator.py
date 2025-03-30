from typing import Any

from sqlalchemy import Column

from src.code_generator.database_model import DataBaseModel


class ServiceGenerator(DataBaseModel):
    def __init__(
        self, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ) -> None:
        super().__init__(model_name, model_attributes, models_file)
        self.repo_file = self.model_name_snake_case + "_" + "repo"

    def get_imports(self) -> str:
        return f"""
import {self.repo_file}\n"""

    def list_query_generator(self) -> str:
        return f"""
def list_{self.model_name_snake_case}s():
    return {self.repo_file}.list_{self.model_name_snake_case}s()\n\n"""

    def get_query_generator(self) -> str:
        primary_key = self.model_primary_keys[0]

        return f"""
def get_{self.model_name_snake_case}({primary_key[0]}):
    return {self.repo_file}.get_{self.model_name_snake_case}({primary_key[0]})\n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.model_name_snake_case}({", ".join(attributes)}):
    return {self.repo_file}.create_{self.model_name_snake_case}({", ".join(attributes)})\n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.model_primary_keys[0][0])
        return f"""
def update_{self.model_name_snake_case}({self.model_primary_keys[0][0]}, {"=None, ".join(attributes[1:])}=None):
    return {self.repo_file}.update_{self.model_name_snake_case}({", ".join(attributes)})\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self.model_name_snake_case}({self.model_primary_keys[0][0]}):
     return {self.repo_file}.delete_{self.model_name_snake_case}({self.model_primary_keys[0][0]})\n\n"""
