"""
sa
"""

import uuid

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UUID, Column, Integer, String

db = SQLAlchemy()


class Org(db.Model):
    """
    dasda
    """

    id: int = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    name: str = Column(String(50), nullable=False)
    public_id: uuid.UUID = Column(UUID, nullable=False, unique=True)

    def __init__(self, name, public_id):
        self.name = name
        self.public_id = public_id


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
