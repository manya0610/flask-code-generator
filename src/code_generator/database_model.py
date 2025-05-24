from typing import Any, Tuple

from sqlalchemy import Column

from src.code_generator.helper import convert_to_snake_case_name


class DataBaseModel:
    model_name: str
    model_attributes: list[Column[Any]]
    model_primary_keys: list[Tuple[str, Any]] = []
    model_name_snake_case: str
    models_file: str
    project_name: str

    def __init__(
        self,
        project_name: str,
        model_name: str,
        model_attributes: list[Column[Any]],
        models_file: str,
    ) -> None:
        self.project_name = project_name
        self.model_name = model_name
        self.model_attributes = model_attributes

        for model_attribute in self.model_attributes:
            if model_attribute.primary_key:
                self.model_primary_keys.append(
                    (str(model_attribute).split(".")[-1], model_attribute.type)
                )

        self.model_name_snake_case = convert_to_snake_case_name(model_name)
        self.models_file = models_file
