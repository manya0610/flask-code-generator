
from src.code_generator.database_model import DataBaseModel


class RepoGenerator:
    _database_model: DataBaseModel

    def __init__(self, database_model:DataBaseModel) -> None:
        self._database_model = database_model

    def get_imports(self) -> str:
        return f"""
import logging
from sqlalchemy import delete, insert, select, update
from src.database import db_session
from {self._database_model.models_file} import {self._database_model.model_name}
logging.basicConfig()
logger = logging.getLogger(__name__)\n"""

    def list_query_generator(self) -> str:
        return f"""
def list_{self._database_model.model_name_snake_case}s():
    try:
        query = select({self._database_model.model_name})
        response = db_session.scalars(query).all()
        return list(response)
    except Exception as e:
        logger.exception("Error while listing {self._database_model.model_name_snake_case}: %s", str(e))
        return []\n\n
        """

    def get_query_generator(self) -> str:
        primary_key = self._database_model.model_primary_keys[0]

        return f"""
def get_{self._database_model.model_name_snake_case}({primary_key[0]}):
    try:
        query = select({self._database_model.model_name}).where({self._database_model.model_name}.{primary_key[0]} == {primary_key[0]})
        response = db_session.scalars(query).one_or_none()
        if response is None:
            logger.warning("{self._database_model.model_name} with {primary_key[0]}=%d not found", {primary_key[0]})
        return response
    except Exception as e:
        logger.exception("Error while getting {self._database_model.model_name} with {primary_key[0]}=%s: %s", {primary_key[0]}, str(e))
        return None
        \n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self._database_model.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self._database_model.model_name_snake_case}({", ".join(attributes)}):
    try:
        query = insert({self._database_model.model_name}).values({", ".join([attribute + "=" + attribute for attribute in attributes])}).returning({self._database_model.model_name})
        response = db_session.scalar(query)
        db_session.commit()
        return response
    except Exception as e:
        db_session.rollback()
        logger.exception("Error creating {self._database_model.model_name} with attributes %s", [{", ".join(attributes)}], str(e))
        return None
        \n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self._database_model.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self._database_model.model_primary_keys[0][0])
        return f"""
def update_{self._database_model.model_name_snake_case}({self._database_model.model_primary_keys[0][0]}, {"=None, ".join(attributes[1:])}=None):
    try:
        values = {{ {", ".join(['"' + attribute + '"' + " : " + attribute for attribute in attributes[1:]])} }}
        values = {{ key: value for key, value in values.items() if value is not None }}

        if not values:
            logger.warning("No fields provided to update for {self._database_model.model_name} with {self._database_model.model_primary_keys[0][0]}=%s", {self._database_model.model_primary_keys[0][0]})
            return None

        query = update({self._database_model.model_name}).where({self._database_model.model_name}.{self._database_model.model_primary_keys[0][0]} == {self._database_model.model_primary_keys[0][0]}).values(values).returning({self._database_model.model_name})
        response = db_session.scalar(query)
        db_session.commit()

        if response is None:
            logger.warning("No {self._database_model.model_name} updated with {self._database_model.model_primary_keys[0][0]}=%s", {self._database_model.model_primary_keys[0][0]})

        return response
    except Exception as e:
        db_session.rollback()
        logger.exception("Error updating {self._database_model.model_name} with {self._database_model.model_primary_keys[0][0]}=%s: %s", {self._database_model.model_primary_keys[0][0]}, str(e))
        return None\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self._database_model.model_name_snake_case}({self._database_model.model_primary_keys[0][0]}):
    try:
        query = delete({self._database_model.model_name}).where({self._database_model.model_name}.{self._database_model.model_primary_keys[0][0]} == {self._database_model.model_primary_keys[0][0]})
        response = db_session.execute(query)
        db_session.commit()

        if response.rowcount == 0:
            logger.warning("No {self._database_model.model_name} found with {self._database_model.model_primary_keys[0][0]}=%s to delete", {self._database_model.model_primary_keys[0][0]})
            return False, 0

        return True, response.rowcount
    except Exception as e:
        db_session.rollback()
        logger.exception("Error deleting {self._database_model.model_name} with {self._database_model.model_primary_keys[0][0]}=%s: %s", {self._database_model.model_primary_keys[0][0]}, str(e))
        return False, 0\n"""
