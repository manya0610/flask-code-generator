from src.code_generator.database_model import DataBaseModel


class FlaskServerGenerator:
    _database_model: DataBaseModel
    controller_file: str
    def __init__(self, database_model:DataBaseModel, controller_file:str) -> None:
        self._database_model = database_model
        self.controller_file = controller_file

    def app_generator(self) -> str:
        return f"""
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    from {self.controller_file} import {self._database_model.model_name_snake_case}_blueprint

    with app.app_context():
        app.register_blueprint({self._database_model.model_name_snake_case}_blueprint)

    return app
\n\n"""
