from src.code_generator.database_model import DataBaseModel
from src.code_generator import constants
class ControllerGenerator:
    database_model: DataBaseModel
    service_file: str
    def __init__(self, database_model:DataBaseModel, service_file:str) -> None:
        self.database_model = database_model
        self.service_file = service_file

    def get_imports(self) -> str:
        return f"""
from {self.database_model.project_name}.{constants.SERVICE_FOLDER} import {self.service_file}
from flask import Blueprint, jsonify, request
from {self.database_model.project_name}.{constants.CONSTANTS_FOLDER}.{constants.CONSTANTS_ERROR_MESSAGE_FILE} import BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND
from {self.database_model.project_name}.{constants.EXCEPTIONS_FOLDER}.{constants.EXCEPTIONS_FILE} import InvalidJSONError, BadRequestError, DatabaseError, NotFoundError
{self.database_model.model_name_snake_case}_blueprint = Blueprint("{self.database_model.model_name_snake_case}", __name__, url_prefix="/{self.database_model.model_name_snake_case}")\n"""
    
    def create_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        return f"""
@{self.database_model.model_name_snake_case}_blueprint.route("/", methods=["POST"])
def create_{self.database_model.model_name_snake_case}_handler():
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise InvalidJSONError
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes])}
        {self.database_model.model_name_snake_case} = {self.service_file}.create_{self.database_model.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self.database_model.model_name_snake_case}.to_dict()), 200
    except (InvalidJSONError,  BadRequestError) as e:
        return jsonify({{"message": BAD_REQUEST,
                        "error" :  e.error_dict}}), 400
    except DatabaseError:
        return jsonify({{"message": INTERNAL_SERVER_ERROR}}), 500
        \n\n"""

    def list_handler_generator(self) -> str:
        return f"""
@{self.database_model.model_name_snake_case}_blueprint.route("/", methods=["GET"])
def list_{self.database_model.model_name_snake_case}s_handler():
    try:
        {self.database_model.model_name_snake_case}_list = {self.service_file}.list_{self.database_model.model_name_snake_case}s()
        return jsonify([{self.database_model.model_name_snake_case}.to_dict() for {self.database_model.model_name_snake_case} in {self.database_model.model_name_snake_case}_list]), 200
    except (InvalidJSONError,  BadRequestError) as e:
        return jsonify({{"message": BAD_REQUEST,
                        "error" :  e.error_dict}}), 400
    except DatabaseError:
        return jsonify({{"message": INTERNAL_SERVER_ERROR}}), 500
        \n\n"""

    def get_handler_generator(self) -> str:
        return f"""
@{self.database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["GET"])
def get_{self.database_model.model_name_snake_case}_handler(id):
    try:
        {self.database_model.model_name_snake_case} = {self.service_file}.get_{self.database_model.model_name_snake_case}(id)
        return jsonify({self.database_model.model_name_snake_case}.to_dict()), 200
    except NotFoundError:
        return jsonify({{"message": NOT_FOUND}}), 404
    except (InvalidJSONError,  BadRequestError) as e:
        return jsonify({{"message": BAD_REQUEST,
                        "error" :  e.error_dict}}), 400
    except DatabaseError:
        return jsonify({{"message": INTERNAL_SERVER_ERROR}}), 500
        \n\n"""

    def update_handler_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.database_model.model_primary_keys[0][0])
        return f"""
@{self.database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["PATCH"])
def update_{self.database_model.model_name_snake_case}_handler(id):
    try:
        request_json = request.get_json(silent=True)
        if request_json is None:
            raise Exception("invalid_json")
        {("\n" + " "*8).join([attribute + " = " + "request_json.get(\"" + attribute + "\"" + ")" for attribute in attributes[1:]])}
        {self.database_model.model_name_snake_case} = {self.service_file}.update_{self.database_model.model_name_snake_case}({", ".join(attributes)})
        return jsonify({self.database_model.model_name_snake_case}.to_dict()), 200
    except NotFoundError:
        return jsonify({{"message": NOT_FOUND}}), 404
    except (InvalidJSONError,  BadRequestError) as e:
        return jsonify({{"message": BAD_REQUEST,
                        "error" :  e.error_dict}}), 400
    except DatabaseError:
        return jsonify({{"message": INTERNAL_SERVER_ERROR}}), 500
    \n\n"""

    def delete_handler_generator(self) -> str:
        return f"""
@{self.database_model.model_name_snake_case}_blueprint.route("/<int:id>", methods=["DELETE"])
def delete_{self.database_model.model_name_snake_case}_handler(id):
    try:
        {self.service_file}.delete_{self.database_model.model_name_snake_case}(id)
        return jsonify(), 200
    except NotFoundError:
        return jsonify({{"message": NOT_FOUND}}), 404
    except (InvalidJSONError,  BadRequestError) as e:
        return jsonify({{"message": BAD_REQUEST,
                        "error" :  e.error_dict}}), 400
    except DatabaseError:
        return jsonify({{"message": INTERNAL_SERVER_ERROR}}), 500
    \n\n"""
