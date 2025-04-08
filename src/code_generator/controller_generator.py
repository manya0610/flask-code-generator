from src.code_generator.database_model import DataBaseModel

class ControllerGenerator:
    _database_model: DataBaseModel
    service_file: str
    service_folder: str
    def __init__(self, database_model:DataBaseModel, service_file:str, service_folder:str) -> None:
        self._database_model = database_model
        self.service_file = service_file
        self.service_folder = service_folder

    def get_imports(self) -> str:
        return f"""
from {self.service_folder} import {self.service_file}
from flask import Blueprint, jsonify, request
{self._database_model.model_name_snake_case}_blueprint = Blueprint("{self._database_model.model_name_snake_case}", __name__, url_prefix="/{self._database_model.model_name_snake_case}")\n"""
    
    def create_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self._database_model.model_attributes
            if not attribute.primary_key
        ]
        return f"""
@{self._database_model.model_name_snake_case}_blueprint.route("/", methods=["POST"])
def create_{self._database_model.model_name_snake_case}_handler():
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise Exception("invalid_json")
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes])}
        {self._database_model.model_name_snake_case} = {self.service_file}.create_{self._database_model.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self._database_model.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(str(e)), 500\n\n"""

    def list_handler_generator(self) -> str:
        return f"""
@{self._database_model.model_name_snake_case}_blueprint.route("/", methods=["GET"])
def list_{self._database_model.model_name_snake_case}s_handler():
    try:
        {self._database_model.model_name_snake_case}_list = {self.service_file}.list_{self._database_model.model_name_snake_case}s()
        return jsonify([{self._database_model.model_name_snake_case}.to_dict() for {self._database_model.model_name_snake_case} in {self._database_model.model_name_snake_case}_list]), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""

    def get_handler_generator(self) -> str:
        return f"""
@{self._database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["GET"])
def get_{self._database_model.model_name_snake_case}_handler(id):
    try:
        {self._database_model.model_name_snake_case} = {self.service_file}.get_{self._database_model.model_name_snake_case}(id)
        return jsonify({self._database_model.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""

    def update_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self._database_model.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self._database_model.model_primary_keys[0][0])
        return f"""
@{self._database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["PATCH"])
def update_{self._database_model.model_name_snake_case}_handler(id):
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise Exception("invalid_json")
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes])}
        {self._database_model.model_name_snake_case} = {self.service_file}.update_{self._database_model.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self._database_model.model_name_snake_case}.to_dict()), 200
    except Exception as e:
        return jsonify(str(e)), 500\n\n"""

    def delete_handler_generator(self) -> str:
        return f"""
@{self._database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_{self._database_model.model_name_snake_case}_handler(id):
    try:
        {self.service_file}.delete_{self._database_model.model_name_snake_case}(id)
        return jsonify(), 200
    except Exception as e:
        return jsonify(e), 500\n\n"""
