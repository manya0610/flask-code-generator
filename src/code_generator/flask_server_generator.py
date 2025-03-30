from typing import Any

from sqlalchemy import Column

from src.code_generator.database_model import DataBaseModel


class FlaskServerGenerator(DataBaseModel):
    def __init__(
        self, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ) -> None:
        super().__init__(model_name, model_attributes, models_file)
        self.controller_file = self.model_name_snake_case + "_" + "controller"

    def app_generator(self) -> str:
        return f"""
from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)
    from {self.controller_file} import {self.model_name_snake_case}_blueprint

    with app.app_context():
        app.register_blueprint({self.model_name_snake_case}_blueprint)

    return app
\n\n"""
