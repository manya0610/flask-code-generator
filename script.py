import importlib
import inspect

from sqlalchemy import Column, Table

from src.code_generator.crud_generator import CRUDGenerator
from src.code_generator.project_generator import ProjectGenerator
from src.code_generator.helper import copy_models_file

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
            base.__name__ == "Base" for base in obj.__bases__
        ):
            models[name] = obj

    return models


# Example usage
if __name__ == "__main__":
    # Adjust the module name according to your file structure
    module_name = "src.database.models"
    models_file = "/".join(module_name.split(".")[:-1]) + "/models.py"

    models = load_models(module_name)
    print(models)
    project_generator = ProjectGenerator("some_project")

    for model_name, model_class in models.items():
        print(model_class.__dict__)
        for key, val in model_class.__dict__.items():
            if isinstance(val, Table):
                print(key, val, "\n")
                table: Table = val
                print("columns", table.columns)
                crud_generator = CRUDGenerator(project_generator.project_name, model_name, table.columns, module_name)
                print(crud_generator._database_model.model_attributes[0])
                crud_generator.repo_file_generator()
                crud_generator.service_file_generator()
                crud_generator.controller_file_generator()
                project_generator._crud_generator_list.append(crud_generator)
    project_generator.flask_server_file_generator()
    project_generator.exceptions_file_generator()
    copy_models_file(models_file, f"{project_generator.project_name}/database/models.py")


