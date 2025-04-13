
class ExceptionGenerator:
    def __init__(self) -> None:
        pass

    def database_exceptions_generator(self):
        return """
class DatabaseError(Exception):

    error_dict = None

    def __init__(self, *args, error_dict: dict = None):
        super().__init__(*args)
        self.error_dict = error_dict

    pass


class DataBaseIntegrityError(DatabaseError):
    error_dict = None

    def __init__(self, *args, error_dict: dict = None):
        super().__init__(*args)
        self.error_dict = error_dict

    pass


class NotFoundError(Exception):
    pass
\n\n"""

    def request_exceptions_generator(self):
        return """
class InvalidJSONError(Exception):
    error_dict = {"data": "invalid_json"}

    def __init__(self, *args, error_dict=None):
        super().__init__(*args)
        self.error_dict = error_dict


class BadRequestError(Exception):
    error_dict = None

    def __init__(self, *args, error_dict=None):
        super().__init__(*args)
        self.error_dict = error_dict
\n\n"""
