from typing import Any

from sqlalchemy import Column


from src.code_generator.database_model import DataBaseModel


class RepoGenerator(DataBaseModel):

    def __init__(self, model_name:str, model_attributes:list[Column[Any]], models_file:str) -> None:
        super().__init__(model_name, model_attributes, models_file)

    def get_imports(self) -> str:
        return f"""
import logging
from sqlalchemy import delete, insert, select, update
from src.database import db_session
from {self.models_file} import {self.model_name}
logging.basicConfig()
logger = logging.getLogger(__name__)\n"""

    def list_query_generator(self) -> str:
        return f"""
def list_{self.model_name_snake_case}():
    try:
        query = select({self.model_name})
        response = db_session.scalars(query).all()
        return list(response)
    except Exception as e:
        logger.exception("Error while listing {self.model_name_snake_case}: %s", str(e))
        return []\n\n
        """

    def get_query_generator(self) -> str:
        primary_key = self.model_primary_keys[0]

        return f"""
def get_{self.model_name_snake_case}({primary_key[0]}):
    try:
        query = select({self.model_name}).where({self.model_name}.{primary_key[0]} == {primary_key[0]})
        response = db_session.scalars(query).one_or_none()
        if response is None:
            logger.warning("{self.model_name} with {primary_key[0]}=%d not found", {primary_key[0]})
        return response
    except Exception as e:
        logger.exception("Error while getting {self.model_name} with {primary_key[0]}=%s: %s", {primary_key[0]}, str(e))
        return None
        \n\n"""

    def create_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        return f"""
def create_{self.model_name_snake_case}({", ".join(attributes)}):
    try:
        query = insert({self.model_name}).values({", ".join([attribute + "=" + attribute for attribute in attributes])}).returning({self.model_name})
        response = db_session.scalar(query)
        db_session.commit()
        return response
    except Exception as e:
        db_session.rollback()
        logger.exception("Error creating {self.model_name} with attributes %s", [{", ".join(attributes)}], str(e))
        return None
        \n\n"""

    def update_query_generator(self) -> str:
        attributes = [
            str(attribute).split(".")[-1]
            for attribute in self.model_attributes
            if not attribute.primary_key
        ]
        attributes.insert(0, self.model_primary_keys[0][0])
        return f"""
def update_{self.model_name_snake_case}({self.model_primary_keys[0][0]}, {"=None, ".join(attributes[1:])}=None):
    try:
        values = {{ {", ".join([ '"' + attribute + '"' + " : " + attribute for attribute in attributes[1:]])} }}
        values = {{ key: value for key, value in values.items() if value is not None }}

        if not values:
            logger.warning("No fields provided to update for {self.model_name} with {self.model_primary_keys[0][0]}=%s", {self.model_primary_keys[0][0]})
            return None

        query = update({self.model_name}).where({self.model_name}.{self.model_primary_keys[0][0]} == {self.model_primary_keys[0][0]}).values(values).returning({self.model_name})
        response = db_session.scalar(query)
        db_session.commit()

        if response is None:
            logger.warning("No {self.model_name} updated with {self.model_primary_keys[0][0]}=%s", {self.model_primary_keys[0][0]})

        return response
    except Exception as e:
        db_session.rollback()
        logger.exception("Error updating {self.model_name} with {self.model_primary_keys[0][0]}=%s: %s", {self.model_primary_keys[0][0]}, str(e))
        return None\n\n"""

    def delete_query_generator(self) -> str:
        return f"""
def delete_{self.model_name_snake_case}({self.model_primary_keys[0][0]}):
    try:
        query = delete({self.model_name}).where({self.model_name}.{self.model_primary_keys[0][0]} == {self.model_primary_keys[0][0]})
        response = db_session.execute(query)
        db_session.commit()

        if response.rowcount == 0:
            logger.warning("No {self.model_name} found with {self.model_primary_keys[0][0]}=%s to delete", {self.model_primary_keys[0][0]})
            return False, 0

        return True, response.rowcount
    except Exception as e:
        db_session.rollback()
        logger.exception("Error deleting {self.model_name} with {self.model_primary_keys[0][0]}=%s: %s", {self.model_primary_keys[0][0]}, str(e))
        return False, 0\n"""