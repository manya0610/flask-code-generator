from typing import Any

from sqlalchemy import Column

from src.code_generator.database_model import DataBaseModel


class ControllerGenerator(DataBaseModel):
    def __init__(
        self, model_name: str, model_attributes: list[Column[Any]], models_file: str
    ) -> None:
        super().__init__(model_name, model_attributes, models_file)
        self.service_file = self.model_name_snake_case + "_" + "service"

    def get_imports(self) -> str:
        return f"""
import {self.service_file}
from flask import Blueprint, jsonify, request
{self.model_name_snake_case}_blueprint = Blueprint("{self.model_name_snake_case}", __name__, url_prefix="/{self.model_name_snake_case}")\n"""
    
    def create_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        return f"""
@{self.model_name_snake_case}_blueprint.route("/", methods=["POST"])
def create_{self.model_name_snake_case}_handler():
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise Exception("invalid_json")
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes])}
        {self.model_name_snake_case} = {self.service_file}.create_{self.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(str(e)), 500\n\n"""

    def list_handler_generator(self) -> str:
        return f"""
@{self.model_name_snake_case}_blueprint.route("/", methods=["GET"])
def list_{self.model_name_snake_case}s_handler():
    try:
        {self.model_name_snake_case}_list = {self.service_file}.list_{self.model_name_snake_case}s()
        return jsonify([{self.model_name_snake_case}.to_dict() for {self.model_name_snake_case} in {self.model_name_snake_case}_list]), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""

    def get_handler_generator(self) -> str:
        return f"""
@{self.model_name_snake_case}_blueprint.route("/<int:id>", methods=["GET"])
def get_{self.model_name_snake_case}_handler(id):
    try:
        {self.model_name_snake_case} = {self.service_file}.get_{self.model_name_snake_case}(id)
        return jsonify({self.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""

    def update_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.model_primary_keys[0][0])
        return f"""
@{self.model_name_snake_case}_blueprint.route("/<int:id>", methods=["PATCH"])
def update_{self.model_name_snake_case}_handler(id):
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise Exception("invalid_json")
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes])}
        {self.model_name_snake_case} = {self.service_file}.update_{self.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(str(e)), 500\n\n"""

    def delete_handler_generator(self) -> str:
        return f"""
@{self.model_name_snake_case}_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_{self.model_name_snake_case}_handler(id):
    try:
        {self.service_file}.delete_{self.model_name_snake_case}(id)
        return jsonify(), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""
