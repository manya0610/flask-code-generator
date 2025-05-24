import re
import shutil


def convert_to_snake_case_name(model_name: str) -> str:
    model_name_snake_case = re.sub(r"([a-z])([A-Z])", r"\1_\2", model_name)
    return model_name_snake_case.lower()


def copy_models_file(source, destination):
    shutil.copyfile(source, destination)
