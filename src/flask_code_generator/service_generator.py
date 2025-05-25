from src.flask_code_generator import constants
from src.flask_code_generator.database_model import DataBaseModel


class ServiceGenerator:
    database_model: DataBaseModel
    repo_file: str

    def __init__(self, database_model: DataBaseModel, repo_file: str) -> None:
        self.database_model = database_model
        self.repo_file = repo_file

    def get_imports(self) -> str:
        return f"""
from {self.database_model.project_name}.{constants.REPO_FOLDER} import {self.repo_file}\n"""

    def list_query_generator(self) -> str:
        return f"""
def list_{self.database_model.model_name_snake_case}s():
    return {self.repo_file}.list_{self.database_model.model_name_snake_case}s()\n\n"""

    def get_query_generator(self) -> str:
        primary_key = self.database_model.model_primary_keys[0]

        return f"""
def get_{self.database_model.model_name_snake_case}({primary_key[0]}):
    return {self.repo_file}.get_{self.database_model.model_name_snake_case}({primary_key[0]})\n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.database_model.model_name_snake_case}({", ".join(attributes)}):
    return {self.repo_file}.create_{self.database_model.model_name_snake_case}({", ".join(attributes)})\n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.database_model.model_primary_keys[0][0])
        return f"""
def update_{self.database_model.model_name_snake_case}({self.database_model.model_primary_keys[0][0]}, {"=None, ".join(attributes[1:])}=None):
    return {self.repo_file}.update_{self.database_model.model_name_snake_case}({", ".join(attributes)})\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self.database_model.model_name_snake_case}({self.database_model.model_primary_keys[0][0]}):
     return {self.repo_file}.delete_{self.database_model.model_name_snake_case}({self.database_model.model_primary_keys[0][0]})\n\n"""
