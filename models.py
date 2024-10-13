"""
sa
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column
db = SQLAlchemy()


class User(db.Model):
    """
    dasda
    """
    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password