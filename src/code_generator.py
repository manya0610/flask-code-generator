import re

from sqlalchemy import Column, Table


class DataBaseModel:
    model_name: str
    model_attributes: list[Column]
    model_primary_keys: list = []
    model_name_snake_case: str
    models_file: str

    def __init__(self, model_name, model_attributes, models_file):
        self.model_name = model_name
        self.model_attributes = model_attributes

        for model_attribute in self.model_attributes:
            if model_attribute.primary_key:
                self.model_primary_keys.append(
                    (str(model_attribute).split(".")[-1], model_attribute.type)
                )

        self.model_name_snake_case = CodeGenerator.convert_to_snake_case_name(
            model_name
        )
        self.models_file = models_file


class ServiceGenerator(DataBaseModel):

    def __init__(self, model_name, model_attributes, models_file):
        super().__init__(model_name, model_attributes, models_file)

    def get_imports(self):
        return f"""
from {self.models_file} import {self.model_name}, db\n"""

    def get_all_query_generator(self):
        return f"""
def get_all_{self.model_name_snake_case}():
    return {self.model_name}.query.all()\n\n"""

    def get_query_generator(self):
        primary_key = self.model_primary_keys[0]

        return f"""
def get_{self.model_name_snake_case}({primary_key[0]}):
    return {self.model_name}.query.filter({self.model_name}.{primary_key[0]} == {primary_key[0]}).one_or_none()\n\n"""

    def create_query_generator(self):
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.model_name_snake_case}({", ".join(attributes)}):
    return {self.model_name}({", ".join(attributes)})\n\n"""

    def update_query_generator(self):
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

    def delete_query_generator(self):
        return f"""
def delete_{self.model_name_snake_case}({self.model_primary_keys[0][0]}):
    {self.model_name_snake_case} = get_{self.model_name_snake_case}({self.model_primary_keys[0][0]})
    if not {self.model_name_snake_case}:
        raise Exception("Not Found")
    db.session.delete({self.model_name_snake_case})
    db.session.commit()\n"""


class CodeGenerator(DataBaseModel):

    _service_generator: ServiceGenerator

    def __init__(self, model_name, model_attributes, models_file):
        super().__init__(model_name, model_attributes, models_file)
        self._service_generator = ServiceGenerator(
            model_name, model_attributes, models_file
        )

    @staticmethod
    def convert_to_snake_case_name(model_name):
        model_name_snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", model_name)
        return model_name_snake_case.lower()

    def service_file_generator(self):
        with open(
            f"{self.model_name_snake_case.lower()}_service.py", "w", encoding="utf-8"
        ) as f:
            f.write(self._service_generator.get_imports())
            f.write(self._service_generator.get_all_query_generator())
            f.write(self._service_generator.get_query_generator())
            f.write(self._service_generator.create_query_generator())
            f.write(self._service_generator.update_query_generator())
            f.write(self._service_generator.delete_query_generator())
