import importlib
import inspect
from sqlalchemy import Column, Table
import re


# Function to get model attributes and types
def get_model_attributes(model):
    attributes = {}

    for attr_name in dir(model):
        if not attr_name.startswith("__"):
            attr = getattr(model, attr_name)
            # Check if the attribute is an instance of Column
            if isinstance(attr, Column):
                attributes[attr_name] = {
                    "type": str(attr.type),
                    "nullable": attr.nullable,
                    "unique": attr.unique,
                }

    return attributes


# Load the models from models.py
def load_models(module_name):
    module = importlib.import_module(module_name)
    models = {}

    # Iterate through all classes in the module
    for name, obj in inspect.getmembers(module, inspect.isclass):
        # Check if the class is a subclass of db.Model
        if hasattr(obj, "__bases__") and any(
            base.__name__ == "Model" for base in obj.__bases__
        ):
            models[name] = obj

    return models


class CodeGenerator:
    model_name: str
    model_attributes: list[Column]
    model_primary_keys: list = []
    model_name_snake_case: str
    models_file:str
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

    @staticmethod
    def convert_to_snake_case_name(model_name):
        model_name_snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", model_name)
        return model_name_snake_case.lower()

    def file_generator(self):
        with open(
            f"{self.model_name_snake_case.lower()}_service.py", "w", encoding="utf-8"
        ) as f:
            f.write(self.get_imports())
            f.write(self.get_all_query_generator())
            f.write(self.get_query_generator())
            f.write(self.create_query_generator())

    def get_imports(self):
        return f"""
from {self.models_file} import {self.model_name}\n"""

    def get_all_query_generator(self):
        return f"""
def get_all_{self.model_name_snake_case}():
    return {self.model_name}.query.all()\n\n"""

    def get_query_generator(self):
        primary_key = self.model_primary_keys[0]

        return f"""
def get_{self.model_name_snake_case}({primary_key[0]}):
    {self.model_name}.query.filter({self.model_name}.{primary_key[0]} == {primary_key[0]}).one()\n\n"""

    def create_query_generator(self):
        attributes = [str(attribute).split(".")[-1] for attribute in self.model_attributes if not attribute.primary_key]
        return f"""
def create_{self.model_name_snake_case}({", ".join(attributes)}):
    return {self.model_name}({", ".join(attributes)})"""

# Example usage
if __name__ == "__main__":
    # Adjust the module name according to your file structure
    module_name = "models"
    models = load_models(module_name)
    print(models)
    for model_name, model_class in models.items():
        print(model_class.__dict__)
        for key, val in model_class.__dict__.items():
            if isinstance(val, Table):
                print(key, val, "\n")
                table: Table = val
                print(table.columns[0])
                code_generator = CodeGenerator(model_name, table.columns, module_name)
                print(code_generator.model_attributes[0])
                code_generator.file_generator()
    #     attrs = get_model_attributes(model_class)
    #     print(f"Model: {model_name}, Attributes: {attrs}")
