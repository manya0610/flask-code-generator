import importlib
import inspect

from sqlalchemy import Column, Table

from flask_code_generator.crud_generator import CRUDGenerator
from flask_code_generator.helper import copy_models_file
from flask_code_generator.project_generator import ProjectGenerator


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
    try:
        # module_name = "database.models"
        module_name = input("Enter models.py File Path as Module: ")

        models_file = "/".join(module_name.split(".")[:-1]) + "/models.py"

        models = load_models(module_name)
        print(models)
        project_name = "some_project"
        if models:
            project_name = input("Enter Project Name: ")
        project_generator = ProjectGenerator(project_name)

        for model_name, model_class in models.items():
            print(model_class.__dict__)
            for key, val in model_class.__dict__.items():
                if isinstance(val, Table):
                    print(key, val, "\n")
                    table: Table = val
                    print("columns", table.columns)
                    crud_generator = CRUDGenerator(
                        project_generator.project_name,
                        model_name,
                        table.columns,
                        module_name,
                    )
                    print(crud_generator.database_model.model_attributes[0])
                    crud_generator.repo_file_generator()
                    crud_generator.service_file_generator()
                    crud_generator.controller_file_generator()
                    project_generator.crud_generator_list.append(crud_generator)
        project_generator.flask_server_file_generator()
        project_generator.exceptions_file_generator()
        project_generator.constants_file_generator()
        project_generator.database_file_generator()
        project_generator.init_file_generator()
        copy_models_file(
            models_file, f"{project_generator.project_name}/database/models.py"
        )
    except ModuleNotFoundError:
        print("given module not found")
