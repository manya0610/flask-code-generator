from src.code_generator.database_model import DataBaseModel


from sqlalchemy import Column


from typing import Any


class ServiceGenerator(DataBaseModel):

    def __init__(self, model_name:str, model_attributes:list[Column[Any]], models_file:str) -> None:
        super().__init__(model_name, model_attributes, models_file)

    def get_imports(self) -> str:
        return f"""
from {self.models_file} import {self.model_name}, db\n"""

    def get_all_query_generator(self) -> str:
        return f"""
def get_all_{self.model_name_snake_case}():
    return {self.model_name}.query.all()\n\n"""

    def get_query_generator(self) -> str:
        primary_key = self.model_primary_keys[0]

        return f"""
def get_{self.model_name_snake_case}({primary_key[0]}):
    return {self.model_name}.query.filter({self.model_name}.{primary_key[0]} == {primary_key[0]}).one_or_none()\n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.model_name_snake_case}({", ".join(attributes)}):
    return {self.model_name}({", ".join(attributes)})\n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.model_primary_keys[0][0])
        return f"""
def update_{self.model_name_snake_case}({self.model_primary_keys[0][0]}, **kwargs):
    {self.model_name_snake_case} = get_{self.model_name_snake_case}({self.model_primary_keys[0][0]})
    if not {self.model_name_snake_case}:
        raise Exception("Not Found")
    for attr, value in kwargs.items():
        setattr({self.model_name_snake_case}, attr, value)
    db.session.commit()
    return {self.model_name_snake_case}\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self.model_name_snake_case}({self.model_primary_keys[0][0]}):
    {self.model_name_snake_case} = get_{self.model_name_snake_case}({self.model_primary_keys[0][0]})
    if not {self.model_name_snake_case}:
        raise Exception("Not Found")
    db.session.delete({self.model_name_snake_case})
    db.session.commit()\n"""