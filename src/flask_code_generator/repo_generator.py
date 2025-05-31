from flask_code_generator import constants
from flask_code_generator.database_model import DataBaseModel


class RepoGenerator:
    database_model: DataBaseModel

    def __init__(self, database_model: DataBaseModel) -> None:
        self.database_model = database_model

    def get_imports(self) -> str:
        return f"""
import logging
from sqlalchemy import delete, insert, select, update
from {self.database_model.project_name}.{constants.DATABASE_FOLDER} import db_session
from {self.database_model.project_name}.{constants.DATABASE_FOLDER}.{constants.MODELS_FILE} import {self.database_model.model_name}
from {self.database_model.project_name}.{constants.EXCEPTIONS_FOLDER}.{constants.EXCEPTIONS_FILE} import NotFoundError, DatabaseError
logging.basicConfig()
logger = logging.getLogger(__name__)\n"""

    def list_query_generator(self) -> str:
        return f"""
def list_{self.database_model.model_name_snake_case}s(limit=100, offset=0):
    try:
        query = select({self.database_model.model_name}).limit(limit).offset(offset)
        response = db_session.scalars(query).all()
        return list(response)
    except Exception as e:
        logger.exception("Error while listing {self.database_model.model_name_snake_case}: %s", str(e))
        raise DatabaseError from e\n\n
        """

    def get_query_generator(self) -> str:
        primary_key = self.database_model.model_primary_keys[0]

        return f"""
def get_{self.database_model.model_name_snake_case}({primary_key[0]}):
    try:
        query = select({self.database_model.model_name}).where({self.database_model.model_name}.{primary_key[0]} == {primary_key[0]})
        response = db_session.scalars(query).one_or_none()
        if response is None:
            logger.warning("{self.database_model.model_name} with {primary_key[0]}=%d not found", {primary_key[0]})
            raise NotFoundError
        return response
    except NotFoundError:
        raise
    except Exception as e:
        logger.exception("Error while getting {self.database_model.model_name} with {primary_key[0]}=%s: %s", {primary_key[0]}, str(e))
        raise DatabaseError from e
        \n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.database_model.model_name_snake_case}({", ".join(attributes)}):
    try:
        query = insert({self.database_model.model_name}).values({", ".join([attribute + "=" + attribute for attribute in attributes])}).returning({self.database_model.model_name})
        response = db_session.scalar(query)
        db_session.commit()
        return response
    except Exception as e:
        db_session.rollback()
        logger.exception("Error creating {self.database_model.model_name} with attributes %s", [{", ".join(attributes)}], str(e))
        raise DatabaseError from e
        \n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.database_model.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.database_model.model_primary_keys[0][0])
        return f"""
def update_{self.database_model.model_name_snake_case}({self.database_model.model_primary_keys[0][0]}, {"=None, ".join(attributes[1:])}=None):
    try:
        values = {{ {", ".join(['"' + attribute + '"' + " : " + attribute for attribute in attributes[1:]])} }}
        values = {{ key: value for key, value in values.items() if value is not None }}

        if not values:
            logger.warning("No fields provided to update for {self.database_model.model_name} with {self.database_model.model_primary_keys[0][0]}=%s", {self.database_model.model_primary_keys[0][0]})
            raise DatabaseError(error_dict={{"{self.database_model.model_name_snake_case}" : "no fields to update"}})

        query = update({self.database_model.model_name}).where({self.database_model.model_name}.{self.database_model.model_primary_keys[0][0]} == {self.database_model.model_primary_keys[0][0]}).values(values).returning({self.database_model.model_name})
        response = db_session.scalar(query)
        db_session.commit()

        if response is None:
            logger.warning("No {self.database_model.model_name} updated with {self.database_model.model_primary_keys[0][0]}=%s", {self.database_model.model_primary_keys[0][0]})
            raise NotFoundError

        return response
    except NotFoundError:
        raise
    except Exception as e:
        db_session.rollback()
        logger.exception("Error updating {self.database_model.model_name} with {self.database_model.model_primary_keys[0][0]}=%s: %s", {self.database_model.model_primary_keys[0][0]}, str(e))
        raise DatabaseError from e\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self.database_model.model_name_snake_case}({self.database_model.model_primary_keys[0][0]}):
    try:
        query = delete({self.database_model.model_name}).where({self.database_model.model_name}.{self.database_model.model_primary_keys[0][0]} == {self.database_model.model_primary_keys[0][0]})
        response = db_session.execute(query)
        db_session.commit()

        if response.rowcount == 0:
            logger.warning("No {self.database_model.model_name} found with {self.database_model.model_primary_keys[0][0]}=%s to delete", {self.database_model.model_primary_keys[0][0]})
            raise NotFoundError

        return True, response.rowcount
    except NotFoundError:
        raise
    except Exception as e:
        db_session.rollback()
        logger.exception("Error deleting {self.database_model.model_name} with {self.database_model.model_primary_keys[0][0]}=%s: %s", {self.database_model.model_primary_keys[0][0]}, str(e))
        raise DatabaseError from e\n"""
