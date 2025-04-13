from src.code_generator import constants
from src.code_generator.crud_generator import CRUDGenerator


class FlaskServerGenerator:
    crud_generator_list: list[CRUDGenerator]
    controller_file: str
    def __init__(self, crud_generator_list:list[CRUDGenerator]) -> None:
        self.crud_generator_list = crud_generator_list


    def controller_imports_generator(self):
        return "    \n".join([f"from {constants.CONTROLLER_FOLDER}.{crud_generator.controller_file} import {crud_generator.database_model.model_name_snake_case}_blueprint" for crud_generator in self.crud_generator_list])
    
    def blueprint_registration_generator(self):
        return "    \n".join([f"app.register_blueprint({crud_generator.database_model.model_name_snake_case}_blueprint)" for crud_generator in self.crud_generator_list])
    def app_generator(self) -> str:
        return f"""
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    {self.controller_imports_generator()}

    with app.app_context():
        {self.blueprint_registration_generator()}

    return app
\n\n"""
